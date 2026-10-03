package ir.muvixo.cmdlogger.velocity;

import net.kyori.adventure.text.Component;
import org.spongepowered.configurate.CommentedConfigurationNode;
import org.spongepowered.configurate.serialize.SerializationException;
import org.spongepowered.configurate.yaml.YamlConfigurationLoader;
import org.slf4j.Logger;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Loads messages.yml, auto-merges any missing keys from the bundled default.
 *
 * Created by Muvixo
 */
public final class Messages {

    private final Path dataDirectory;
    private final Logger logger;
    private final Map<String, String> defaults = new LinkedHashMap<>();
    private CommentedConfigurationNode root;
    private Path file;

    public Messages(Path dataDirectory, Logger logger) {
        this.dataDirectory = dataDirectory;
        this.logger = logger;
    }

    /** Load messages.yml, creating it from the bundled default if missing. */
    public void load() {
        this.file = dataDirectory.resolve("messages.yml");

        // 1. Extract the bundled default into memory (for merge + first write).
        String bundled = readBundled();
        parseDefaults(bundled);

        // 2. If file doesn't exist, write the bundled default verbatim.
        if (!Files.exists(file)) {
            try {
                Files.createDirectories(dataDirectory);
                Files.write(file, bundled.getBytes(StandardCharsets.UTF_8));
            } catch (IOException e) {
                logger.error("Could not write default messages.yml", e);
            }
        }

        // 3. Load user file.
        try {
            root = YamlConfigurationLoader.builder().path(file).build().load();
        } catch (IOException e) {
            logger.error("Could not load messages.yml", e);
            return;
        }

        // 4. Merge: append any missing keys to the user file.
        int added = mergeMissingKeys();
        if (added > 0) {
            try {
                YamlConfigurationLoader.builder().path(file).build().save(root);
                logger.info("[CommandLogger] Added {} missing message key(s) to messages.yml", added);
            } catch (IOException e) {
                logger.warn("[CommandLogger] Could not save merged messages.yml: {}", e.getMessage());
            }
        }
    }

    private String readBundled() {
        try (InputStream in = getClass().getResourceAsStream("/messages.yml")) {
            if (in == null) return "# messages.yml not found in jar\n";
            return new String(in.readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            return "# error reading default messages.yml\n";
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
            // strip surrounding quotes
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
            if (root.node(e.getKey()).virtual()) {
                try {
                    root.node(e.getKey()).set(e.getValue());
                    added++;
                } catch (SerializationException ignored) {}
            }
        }
        return added;
    }

    /** Raw string lookup. Never returns null. */
    public String raw(String key) {
        if (root == null) return defaults.getOrDefault(key, "");
        String v = root.node(key).getString();
        if (v == null) v = defaults.getOrDefault(key, "");
        return v;
    }

    /** Raw string with {placeholder} replacement. */
    public String raw(String key, Object... kv) {
        String s = raw(key);
        for (int i = 0; i + 1 < kv.length; i += 2) {
            s = s.replace("{" + kv[i] + "}", String.valueOf(kv[i + 1]));
        }
        return s;
    }

    /** Colored Component version. */
    public Component get(String key) {
        return ColorUtil.color(raw(key));
    }

    /** Colored Component version with placeholders. */
    public Component get(String key, Object... kv) {
        return ColorUtil.color(raw(key, kv));
    }
}
