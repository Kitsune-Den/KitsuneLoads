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

        // Only the file names are kept ~ the game loads the picture itself from the
        // @modfolder path, so nothing gets decoded into memory up front.
        public static void ScanImages()
        {
            Files.Clear();

            if (!Directory.Exists(ResourceDir))
            {
                Debug.LogWarning($"[KitsuneLoads] Resources directory not found: {ResourceDir}");
                return;
            }

            Files.AddRange(Directory.GetFiles(ResourceDir)
                .Where(p => Extensions.Contains(Path.GetExtension(p).ToLowerInvariant()))
                .Select(Path.GetFileName)
                .OrderBy(n => n, StringComparer.OrdinalIgnoreCase));

            Debug.Log($"[KitsuneLoads] Found {Files.Count} loading-screen images in {ResourceDir}");
        }

        // Shuffle-bag pick ~ every image shows once before any repeats.
        public static string PickNext()
        {
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
