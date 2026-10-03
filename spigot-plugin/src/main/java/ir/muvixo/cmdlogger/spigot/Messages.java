package ir.muvixo.cmdlogger.spigot;

import org.bukkit.ChatColor;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.configuration.file.YamlConfiguration;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Loads messages.yml, auto-merges any missing keys from the bundled default.
 *
 * Created by Muvixo
 */
public final class Messages {

    private final CommandLogger plugin;
    private final Map<String, String> defaults = new LinkedHashMap<>();
    private FileConfiguration cfg;
    private File file;

    public Messages(CommandLogger plugin) {
        this.plugin = plugin;
    }

    public void load() {
        if (!plugin.getDataFolder().exists()) {
            plugin.getDataFolder().mkdirs();
        }

        this.file = new File(plugin.getDataFolder(), "messages.yml");
        String bundled = readBundled();
        parseDefaults(bundled);

        if (!file.exists()) {
            plugin.saveResource("messages.yml", false);
        }

        this.cfg = YamlConfiguration.loadConfiguration(file);

        int added = mergeMissingKeys();
        if (added > 0) {
            try {
                cfg.save(file);
                plugin.getLogger().info("[CommandLogger] Added " + added + " missing message key(s).");
            } catch (IOException e) {
                plugin.getLogger().warning("Could not save merged messages.yml: " + e.getMessage());
            }
        }
    }

    private String readBundled() {
        try (InputStream in = plugin.getResource("messages.yml")) {
            if (in == null) return "# missing\n";
            java.io.ByteArrayOutputStream bos = new java.io.ByteArrayOutputStream();
            byte[] buf = new byte[4096];
            int n;
            while ((n = in.read(buf)) > 0) bos.write(buf, 0, n);
            return new String(bos.toByteArray(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            return "# error\n";
        }
    }

    private void parseDefaults(String yaml) {
        defaults.clear();
        YamlConfiguration temp = new YamlConfiguration();
        try {
            temp.loadFromString(yaml);
        } catch (Exception e) {
            return;
        }
        for (String key : temp.getKeys(true)) {
            Object v = temp.get(key);
            if (v instanceof String) {
                defaults.put(key, (String) v);
            }
        }
    }

    private int mergeMissingKeys() {
        int added = 0;
        for (Map.Entry<String, String> e : defaults.entrySet()) {
            if (!cfg.contains(e.getKey())) {
                cfg.set(e.getKey(), e.getValue());
                added++;
            }
        }
        return added;
    }

    public String raw(String key) {
        if (cfg == null) return defaults.getOrDefault(key, "");
        String v = cfg.getString(key);
        if (v == null) v = defaults.getOrDefault(key, "");
        return v;
    }

    public String raw(String key, Object... kv) {
        String s = raw(key);
        for (int i = 0; i + 1 < kv.length; i += 2) {
            s = s.replace("{" + kv[i] + "}", String.valueOf(kv[i + 1]));
        }
        return s;
    }

    /** Colored string for Spigot (legacy only). */
    public String color(String key) {
        return ChatColor.translateAlternateColorCodes('&', raw(key));
    }

    public String color(String key, Object... kv) {
        return ChatColor.translateAlternateColorCodes('&', raw(key, kv));
    }
}
