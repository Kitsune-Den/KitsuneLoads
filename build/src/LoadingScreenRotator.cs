using System;
using System.Collections.Generic;
using System.IO;
using HarmonyLib;
using UnityEngine;

namespace KitsuneLoads
{
    public class KitsuneLoadsInit : IModApi
    {
        public void InitMod(Mod _modInstance)
        {
            Debug.Log("[KitsuneLoads] Init starting");

            LoadingScreenRotator.ResourceDir = Path.Combine(_modInstance.Path, "Resources");
            LoadingScreenRotator.CacheTextures();

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
        public static string ResourceDir;

        public static readonly string[] ImageFiles =
        {
            "burned_forest_ruins.png",
            "desert_highway_wrecks.png",
            "desert_schoolbus.png",
            "feral_wolf.png",
            "infected_vulture.png",
            "overgrown_city_street.png",
            "ruined_city_skyline.png",
            "screamer_zombie.png",
            "snow_cougar.png",
            "snowy_outpost_camp.png",
            "wooden_fortress.png",
            "zombie_cop.png",
            "zombie_skull_face.png",
        };

        private static readonly List<Texture2D> Cache = new List<Texture2D>();
        private static readonly System.Random Rand = new System.Random();

        public static void CacheTextures()
        {
            Cache.Clear();
            foreach (var file in ImageFiles)
            {
                var path = Path.Combine(ResourceDir, file);
                if (!File.Exists(path))
                {
                    Debug.LogWarning($"[KitsuneLoads] Missing image: {path}");
                    continue;
                }
                var bytes = File.ReadAllBytes(path);
                var tex = new Texture2D(2, 2, TextureFormat.RGBA32, false);
                if (tex.LoadImage(bytes))
                {
                    tex.name = Path.GetFileNameWithoutExtension(file);
                    Cache.Add(tex);
                }
                else
                {
                    Debug.LogWarning($"[KitsuneLoads] Failed to decode: {file}");
                }
            }
            Debug.Log($"[KitsuneLoads] Cached {Cache.Count} loading-screen textures");
        }

        public static Texture2D PickRandom()
        {
            if (Cache.Count == 0) return null;
            return Cache[Rand.Next(Cache.Count)];
        }

        public static string CurrentPickName;
    }

    [HarmonyPatch(typeof(XUiC_LoadingScreen), "OnOpen")]
    public static class LoadingScreen_OnOpen_Patch
    {
        public static void Postfix(XUiC_LoadingScreen __instance)
        {
            var pick = LoadingScreenRotator.PickRandom();
            if (pick == null) return;
            LoadingScreenRotator.CurrentPickName = pick.name;
            Debug.Log($"[KitsuneLoads] OnOpen — rolled '{pick.name}'");
        }
    }

    [HarmonyPatch(typeof(XUiC_LoadingScreen), "GetBindingValueInternal")]
    public static class LoadingScreen_GetBindingValueInternal_Patch
    {
        private static bool _loggedOnce = false;

        public static bool Prefix(ref bool __result, ref string _value, string _bindingName)
        {
            if (_bindingName != "background_texture") return true;

            var name = LoadingScreenRotator.CurrentPickName;
            if (string.IsNullOrEmpty(name)) return true;

            _value = $"@modfolder(KitsuneLoads):Resources/{name}.png";
            __result = true;

            if (!_loggedOnce)
            {
                _loggedOnce = true;
                Debug.Log($"[KitsuneLoads] Binding intercepted: background_texture -> '{_value}'");
            }
            return false;
        }
    }
}
