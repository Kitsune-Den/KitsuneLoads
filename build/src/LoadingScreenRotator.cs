using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using HarmonyLib;
using UnityEngine;

namespace KitsuneLoads
{
    public class KitsuneLoadsInit : IModApi
    {
        public void InitMod(Mod _modInstance)
        {
            Debug.Log("[KitsuneLoads] Init starting");

            LoadingScreenRotator.ModName = _modInstance.Name;
            LoadingScreenRotator.ResourceDir = Path.Combine(_modInstance.Path, "Resources");
            LoadingScreenRotator.ScanImages();

            try
            {
                var harmony = new Harmony("kitsune.loads");
                harmony.PatchAll();
                Debug.Log("[KitsuneLoads] Harmony patches registered");
            }
            catch (Exception e)
            {
                Debug.LogWarning($"[KitsuneLoads] Harmony.PatchAll threw: {e}");
            }
        }
    }

    public static class LoadingScreenRotator
    {
        public static string ModName;
        public static string ResourceDir;
        public static string CurrentPick;

        private static readonly string[] Extensions = { ".png", ".jpg", ".jpeg" };
        private static readonly List<string> Files = new List<string>();
        private static readonly List<string> Bag = new List<string>();
        private static readonly System.Random Rand = new System.Random();

        // A pack with Resources/seasons.txt keeps its pictures in one folder per season
        // and shows the folder that matches the real-world date. Null = a plain pack.
        private static List<SeasonRule> _rules;
        private static DateTime? _dateOverride;
        private static DateTime _scannedFor = DateTime.MinValue;

        // Only the file names are kept ~ the game loads the picture itself from the
        // @modfolder path, so nothing gets decoded into memory up front.
        public static void ScanImages()
        {
            Files.Clear();
            Bag.Clear();

            if (!Directory.Exists(ResourceDir))
            {
                Debug.LogWarning($"[KitsuneLoads] Resources directory not found: {ResourceDir}");
                return;
            }

            _rules = SeasonRule.Load(Path.Combine(ResourceDir, "seasons.txt"), out _dateOverride);
            _scannedFor = Today();
            var season = _rules == null ? null : SeasonRule.Match(_rules, _scannedFor);

            if (season != null)
            {
                AddImages(Path.Combine(ResourceDir, season), season + "/");
                Debug.Log($"[KitsuneLoads] {_scannedFor:yyyy-MM-dd} is season '{season}'");
            }
            if (_rules != null && Files.Count == 0)
            {
                // No season covers today, or its folder is empty ~ show every season.
                foreach (var dir in Directory.GetDirectories(ResourceDir).OrderBy(d => d, StringComparer.OrdinalIgnoreCase))
                    AddImages(dir, Path.GetFileName(dir) + "/");
                Debug.Log($"[KitsuneLoads] No season pictures for {_scannedFor:yyyy-MM-dd} ~ using every picture");
            }
            if (Files.Count == 0) AddImages(ResourceDir, "");

            Debug.Log($"[KitsuneLoads] Found {Files.Count} loading-screen images in {ResourceDir}");
        }

        private static void AddImages(string dir, string prefix)
        {
            if (!Directory.Exists(dir)) return;
            Files.AddRange(Directory.GetFiles(dir)
                .Where(p => Extensions.Contains(Path.GetExtension(p).ToLowerInvariant()))
                .Select(p => prefix + Path.GetFileName(p))
                .OrderBy(n => n, StringComparer.OrdinalIgnoreCase));
        }

        private static DateTime Today() => _dateOverride ?? DateTime.Now.Date;

        // Shuffle-bag pick ~ every image shows once before any repeats.
        public static string PickNext()
        {
            // A seasonal pack looks at the calendar again when the day changes mid-session.
            if (_rules != null && Today() != _scannedFor) ScanImages();

            if (Files.Count == 0) return null;
            if (Bag.Count == 0)
            {
                Bag.AddRange(Files.OrderBy(_ => Rand.Next()));
                if (Bag.Count > 1 && Bag[0] == CurrentPick)
                {
                    Bag.Add(Bag[0]);
                    Bag.RemoveAt(0);
                }
            }
            var pick = Bag[0];
            Bag.RemoveAt(0);
            return pick;
        }
    }

    // One line of seasons.txt: "Folder = from .. to". Each end is a month-day ("12-01")
    // or a day counted from Lunar New Year ("lunar", "lunar-7", "lunar+15"). Both ends
    // are inclusive, a range may run over the year end, and the first line that covers
    // today wins. "date = 2027-02-06" pretends it is that day, to preview a season.
    public class SeasonRule
    {
        public string Folder;
        public string From;
        public string To;

        // Lunar New Year (Gregorian month, day) ~ other years ask the .NET calendar.
        private static readonly Dictionary<int, int[]> LunarNewYear = new Dictionary<int, int[]>
        {
            { 2025, new[] { 1, 29 } }, { 2026, new[] { 2, 17 } }, { 2027, new[] { 2, 6 } },
            { 2028, new[] { 1, 26 } }, { 2029, new[] { 2, 13 } }, { 2030, new[] { 2, 3 } },
            { 2031, new[] { 1, 23 } }, { 2032, new[] { 2, 11 } }, { 2033, new[] { 1, 31 } },
            { 2034, new[] { 2, 19 } }, { 2035, new[] { 2, 8 } }, { 2036, new[] { 1, 28 } },
        };

        public static List<SeasonRule> Load(string path, out DateTime? dateOverride)
        {
            dateOverride = null;
            if (!File.Exists(path)) return null;

            var rules = new List<SeasonRule>();
            foreach (var raw in File.ReadAllLines(path))
            {
                var line = raw.Split('#')[0].Trim();
                if (line.Length == 0) continue;

                var eq = line.IndexOf('=');
                var key = eq < 0 ? "" : line.Substring(0, eq).Trim();
                var value = eq < 0 ? "" : line.Substring(eq + 1).Trim();

                if (key.Equals("date", StringComparison.OrdinalIgnoreCase))
                {
                    if (DateTime.TryParseExact(value, "yyyy-MM-dd", System.Globalization.CultureInfo.InvariantCulture,
                            System.Globalization.DateTimeStyles.None, out var d))
                        dateOverride = d;
                    else
                        Debug.LogWarning($"[KitsuneLoads] seasons.txt: date must be yyyy-MM-dd, got '{value}'");
                    continue;
                }

                var ends = value.Split(new[] { ".." }, StringSplitOptions.None);
                var rule = new SeasonRule { Folder = key, From = ends[0], To = ends[ends.Length - 1] };
                if (key.Length == 0 || ends.Length != 2 || !Resolve(rule.From, 2028).HasValue || !Resolve(rule.To, 2028).HasValue)
                {
                    Debug.LogWarning($"[KitsuneLoads] seasons.txt: can't read '{line}'");
                    continue;
                }
                rules.Add(rule);
            }
            return rules;
        }

        public static string Match(List<SeasonRule> rules, DateTime today)
        {
            foreach (var rule in rules)
            {
                // The range that holds today started this year or last year.
                for (var year = today.Year; year >= today.Year - 1; year--)
                {
                    var from = Resolve(rule.From, year);
                    var to = Resolve(rule.To, year);
                    if (to < from) to = Resolve(rule.To, year + 1);
                    if (from.HasValue && to.HasValue && today >= from && today <= to) return rule.Folder;
                }
            }
            return null;
        }

        // The day an end of a range falls on in the given year, or null if it can't be read.
        private static DateTime? Resolve(string token, int year)
        {
            token = token.Replace(" ", "").ToLowerInvariant();
            if (token.StartsWith("lunar"))
            {
                var offset = 0;
                if (token.Length > 5 && !int.TryParse(token.Substring(5), out offset)) return null;
                return LunarDate(year)?.AddDays(offset);
            }

            var parts = token.Split('-');
            if (parts.Length != 2 || !int.TryParse(parts[0], out var month) || !int.TryParse(parts[1], out var day)) return null;
            if (month < 1 || month > 12 || day < 1 || day > 31) return null;
            return new DateTime(year, month, Math.Min(day, DateTime.DaysInMonth(year, month)));
        }

        private static DateTime? LunarDate(int year)
        {
            if (LunarNewYear.TryGetValue(year, out var md)) return new DateTime(year, md[0], md[1]);
            try
            {
                return new System.Globalization.ChineseLunisolarCalendar().ToDateTime(year, 1, 1, 0, 0, 0, 0);
            }
            catch (Exception)
            {
                return null;
            }
        }
    }

    // V3.x dropped GetBindingValueInternal ~ {background_texture} is now the
    // [XuiXmlBinding] property CurrentBackground. We roll a picture before vanilla's
    // OnOpen runs its RefreshBindings, then answer the property getter with our path.
    // Overriding the getter (rather than the currentBackground field) keeps our picture
    // even when the server sends its own loadingscreen.xml or another mod re-rolls it.
    [HarmonyPatch(typeof(XUiC_LoadingScreen), nameof(XUiC_LoadingScreen.OnOpen))]
    public static class LoadingScreen_OnOpen_Patch
    {
        public static void Prefix()
        {
            var pick = LoadingScreenRotator.PickNext();
            if (pick == null) return;
            LoadingScreenRotator.CurrentPick = pick;
            Debug.Log($"[KitsuneLoads] OnOpen ~ rolled '{pick}'");
        }
    }

    [HarmonyPatch(typeof(XUiC_LoadingScreen), nameof(XUiC_LoadingScreen.CurrentBackground), MethodType.Getter)]
    public static class LoadingScreen_CurrentBackground_Patch
    {
        private static bool _loggedOnce = false;

        public static void Postfix(ref string __result)
        {
            var name = LoadingScreenRotator.CurrentPick;
            if (string.IsNullOrEmpty(name)) return;

            __result = $"@modfolder({LoadingScreenRotator.ModName}):Resources/{name}";

            if (!_loggedOnce)
            {
                _loggedOnce = true;
                Debug.Log($"[KitsuneLoads] Binding intercepted: background_texture -> '{__result}'");
            }
        }
    }
}
