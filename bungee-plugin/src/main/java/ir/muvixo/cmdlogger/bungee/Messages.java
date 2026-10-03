package ir.muvixo.cmdlogger.bungee;

import net.md_5.bungee.config.Configuration;
import net.md_5.bungee.config.ConfigurationProvider;
import net.md_5.bungee.config.YamlConfiguration;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
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
    private Configuration cfg;
    private File file;

    public Messages(CommandLogger plugin) {
        this.plugin = plugin;
    }

    public void load() {
        this.file = new File(plugin.getDataFolder(), "messages.yml");
        String bundled = readBundled();
        parseDefaults(bundled);

        if (!file.exists()) {
            try {
                plugin.getDataFolder().mkdirs();
                Files.write(file.toPath(), bundled.getBytes(StandardCharsets.UTF_8));
            } catch (IOException e) {
                plugin.getLogger().severe("Could not write default messages.yml: " + e.getMessage());
            }
        }

        try {
            cfg = ConfigurationProvider.getProvider(YamlConfiguration.class).load(file);
        } catch (IOException e) {
            plugin.getLogger().severe("Could not load messages.yml: " + e.getMessage());
            return;
        }

        int added = mergeMissingKeys();
        if (added > 0) {
            try {
                ConfigurationProvider.getProvider(YamlConfiguration.class).save(cfg, file);
                plugin.getLogger().info("[CommandLogger] Added " + added + " missing message key(s).");
            } catch (IOException e) {
                plugin.getLogger().warning("Could not save merged messages.yml: " + e.getMessage());
            }
        }
    }

    private String readBundled() {
        try (InputStream in = plugin.getResourceAsStream("messages.yml")) {
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
        for (String line : yaml.split("\n")) {
            String trimmed = line.trim();
            if (trimmed.isEmpty() || trimmed.startsWith("#")) continue;
            int colon = trimmed.indexOf(':');
            if (colon <= 0) continue;
            String key = trimmed.substring(0, colon).trim();
            String value = trimmed.substring(colon + 1).trim();
            if (value.length() >= 2
                    && ((value.startsWith("\"") && value.endsWith("\""))
                     || (value.startsWith("'") && value.endsWith("'")))) {
                value = value.substring(1, value.length() - 1);
            }
            if (!key.isEmpty()) defaults.put(key, value);
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
}
