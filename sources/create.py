
#!/usr/bin/env python3
"""
create_plugin.py - Generates the complete CommandLogger project structure
including Velocity, BungeeCord 1.8, Spigot, and Paper support.

Author: muvixo
Usage: python create_plugin.py
"""

import os
import sys

# ============================================================
#  PROJECT ROOT
# ============================================================
ROOT = os.path.dirname(os.path.abspath(__file__))

# ============================================================
#  FILE CONTENTS
# ============================================================

GITHUB_BUILD_YML = """name: Build Plugins

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'
          cache: maven

      - name: Build all modules
        run: mvn -B clean package --file pom.xml

      - name: Upload Velocity plugin
        uses: actions/upload-artifact@v4
        with:
          name: commandlogger-velocity
          path: velocity-plugin/target/commandlogger-velocity-*.jar
          if-no-files-found: error

      - name: Upload BungeeCord plugin
        uses: actions/upload-artifact@v4
        with:
          name: commandlogger-bungee
          path: bungee-plugin/target/commandlogger-bungee-*.jar
          if-no-files-found: error

      - name: Upload Spigot plugin
        uses: actions/upload-artifact@v4
        with:
          name: commandlogger-spigot
          path: spigot-plugin/target/commandlogger-spigot-*.jar
          if-no-files-found: error

      - name: Upload Paper plugin
        uses: actions/upload-artifact@v4
        with:
          name: commandlogger-paper
          path: paper-plugin/target/commandlogger-paper-*.jar
          if-no-files-found: error
"""

GITIGNORE = """target/
.idea/
*.iml
*.log
.DS_Store
.vscode/
"""

LICENSE = """MIT License

Copyright (c) 2024 muvixo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

README = """# CommandLogger v2.2

Logs **every command** any player types on any backend server and broadcasts
them to staff / OP players on the proxy.

Supports **Velocity**, **BungeeCord 1.8+**, **Spigot 1.8+**, and **Paper 1.8+**.

**Author:** muvixo

## What's new in v2.2

- **BungeeCord 1.8 support** - full plugin messaging + OP tracking.
- **Paper support** - native Paper 1.8+ backend plugin.
- **Bulletproof OP detection** - OP status is attached to *every* command.
- **UUID-based tracking** - no more name-change or case bugs.
- **`/clogs op <player>` / `/clogs unop <player>`** - manual overrides.
- **`/clogs list`** - see all currently tracked OPs.
- **`force-see-players`** - a config list of players who always see logs.

## Modules

| Module | Target | Java |
|--------|--------|------|
| `velocity-plugin` | Velocity 3.x | 17 |
| `bungee-plugin` | BungeeCord 1.8+ | 8 |
| `spigot-plugin` | Spigot 1.8.8 | 8 |
| `paper-plugin` | Paper 1.8.8+ | 8 |

## Commands (Proxy)

| Command | Description |
|---------|-------------|
| `/clogs` | Show plugin info |
| `/clogs help` | Show help |
| `/clogs reload` | Reload config |
| `/clogs debug <player>` | Diagnose a player's permissions |
| `/clogs status <player>` | Same as debug |
| `/clogs op <player>` | Manually mark player as OP |
| `/clogs unop <player>` | Manually unmark player |
| `/clogs list` | List all tracked OPs |

## Build

```bash
mvn clean package
```

Outputs:
- `velocity-plugin/target/commandlogger-velocity-2.2.0.jar`
- `bungee-plugin/target/commandlogger-bungee-2.2.0.jar`
- `spigot-plugin/target/commandlogger-spigot-2.2.0.jar`
- `paper-plugin/target/commandlogger-paper-2.2.0.jar`

## Setup

### 1. Install the proxy plugin
- **Velocity:** drop `commandlogger-velocity-2.2.0.jar` into `plugins/`
- **BungeeCord:** drop `commandlogger-bungee-2.2.0.jar` into `plugins/`

### 2. Install the backend plugin
- **Spigot:** drop `commandlogger-spigot-2.2.0.jar` into `plugins/`
- **Paper:** drop `commandlogger-paper-2.2.0.jar` into `plugins/`

### 3. Configure
Make sure `channel` matches on both proxy and backend configs.
Default: `commandlogger:main`

### 4. Register the channel (BungeeCord)
In your BungeeCord `config.yml`, ensure `bungeecord: true` is set on the
Spigot/Paper backend servers so plugin messaging works.
"""

# ============================================================
#  PARENT POM
# ============================================================
PARENT_POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>ir.muvixo</groupId>
    <artifactId>commandlogger-parent</artifactId>
    <version>2.2.0</version>
    <packaging>pom</packaging>
    <name>CommandLogger Parent</name>

    <modules>
        <module>velocity-plugin</module>
        <module>bungee-plugin</module>
        <module>spigot-plugin</module>
        <module>paper-plugin</module>
    </modules>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
    </properties>

    <repositories>
        <repository>
            <id>papermc</id>
            <url>https://repo.papermc.io/repository/maven-public/</url>
        </repository>
        <repository>
            <id>spigotmc-repo</id>
            <url>https://hub.spigotmc.org/nexus/content/repositories/snapshots/</url>
        </repository>
        <repository>
            <id>sonatype</id>
            <url>https://oss.sonatype.org/content/groups/public/</url>
        </repository>
        <repository>
            <id>codemc</id>
            <url>https://repo.codemc.io/repository/maven-public/</url>
        </repository>
        <repository>
            <id>sonatype-oss</id>
            <url>https://s01.oss.sonatype.org/content/repositories/snapshots/</url>
        </repository>
    </repositories>

    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.11.0</version>
                </plugin>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-shade-plugin</artifactId>
                    <version>3.5.1</version>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
"""

# ============================================================
#  VELOCITY PLUGIN
# ============================================================
VELOCITY_POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>ir.muvixo</groupId>
        <artifactId>commandlogger-parent</artifactId>
        <version>2.2.0</version>
    </parent>

    <artifactId>commandlogger-velocity</artifactId>
    <packaging>jar</packaging>
    <name>CommandLogger (Velocity)</name>

    <dependencies>
        <dependency>
            <groupId>com.velocitypowered</groupId>
            <artifactId>velocity-api</artifactId>
            <version>3.3.0-SNAPSHOT</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.spongepowered</groupId>
            <artifactId>configurate-yaml</artifactId>
            <version>4.1.2</version>
        </dependency>
    </dependencies>

    <build>
        <finalName>${project.artifactId}-${project.version}</finalName>
        <resources>
            <resource>
                <directory>src/main/resources</directory>
                <filtering>true</filtering>
                <includes>
                    <include>velocity-plugin.json</include>
                </includes>
            </resource>
            <resource>
                <directory>src/main/resources</directory>
                <filtering>false</filtering>
                <excludes>
                    <exclude>velocity-plugin.json</exclude>
                </excludes>
            </resource>
        </resources>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <release>17</release>
                </configuration>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals><goal>shade</goal></goals>
                        <configuration>
                            <createDependencyReducedPom>false</createDependencyReducedPom>

                            <filters>
                                <filter>
                                    <artifact>*:*</artifact>
                                    <excludes>
                                        <exclude>META-INF/*.SF</exclude>
                                        <exclude>META-INF/*.DSA</exclude>
                                        <exclude>META-INF/*.RSA</exclude>
                                        <exclude>META-INF/*.EC</exclude>
                                        <exclude>META-INF/MANIFEST.MF</exclude>
                                        <exclude>module-info.class</exclude>
                                        <exclude>META-INF/versions/*/module-info.class</exclude>
                                    </excludes>
                                </filter>
                            </filters>

                            <relocations>
                                <relocation>
                                    <pattern>org.spongepowered.configurate</pattern>
                                    <shadedPattern>ir.muvixo.cmdlogger.libs.configurate</shadedPattern>
                                </relocation>
                                <relocation>
                                    <pattern>io.leangen.geantyref</pattern>
                                    <shadedPattern>ir.muvixo.cmdlogger.libs.geantyref</shadedPattern>
                                </relocation>
                                <relocation>
                                    <pattern>org.yaml.snakeyaml</pattern>
                                    <shadedPattern>ir.muvixo.cmdlogger.libs.snakeyaml</shadedPattern>
                                </relocation>
                            </relocations>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
"""

VELOCITY_JSON = """{
  "id": "commandlogger",
  "name": "CommandLogger",
  "version": "${project.version}",
  "description": "Broadcasts commands from backend Spigot servers to staff",
  "authors": ["muvixo"],
  "main": "ir.muvixo.cmdlogger.velocity.CommandLogger"
}
"""

VELOCITY_MAIN = """package ir.muvixo.cmdlogger.velocity;

import com.google.inject.Inject;
import com.velocitypowered.api.command.CommandManager;
import com.velocitypowered.api.event.Subscribe;
import com.velocitypowered.api.event.proxy.ProxyInitializeEvent;
import com.velocitypowered.api.event.proxy.ProxyShutdownEvent;
import com.velocitypowered.api.plugin.Plugin;
import com.velocitypowered.api.plugin.annotation.DataDirectory;
import com.velocitypowered.api.proxy.ProxyServer;
import com.velocitypowered.api.proxy.messages.MinecraftChannelIdentifier;
import org.slf4j.Logger;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

@Plugin(
        id = "commandlogger",
        name = "CommandLogger",
        version = "2.2.0",
        description = "Broadcasts commands from backend Spigot servers to staff",
        authors = {"muvixo"}
)
public class CommandLogger {

    private final ProxyServer server;
    private final Logger logger;
    private final Path dataDirectory;

    private Config config;
    private OpPlayerManager opManager;
    private PermissionChecker permissionChecker;
    private BackendMessageReceiver receiver;
    private MinecraftChannelIdentifier channel;

    @Inject
    public CommandLogger(ProxyServer server, Logger logger, @DataDirectory Path dataDirectory) {
        this.server = server;
        this.logger = logger;
        this.dataDirectory = dataDirectory;
    }

    @Subscribe
    public void onProxyInitialize(ProxyInitializeEvent event) {
        try {
            if (!Files.exists(dataDirectory)) {
                Files.createDirectories(dataDirectory);
            }
        } catch (IOException e) {
            logger.error("Could not create data directory", e);
        }

        this.config = new Config(dataDirectory, logger);
        this.config.load();

        this.opManager = new OpPlayerManager(server, logger, config);
        server.getEventManager().register(this, opManager);

        this.permissionChecker = new PermissionChecker(config, opManager, logger);

        this.channel = MinecraftChannelIdentifier.from(config.getChannel());
        server.getChannelRegistrar().register(channel);
        this.receiver = new BackendMessageReceiver(server, logger, config, opManager, permissionChecker);
        server.getEventManager().register(this, receiver);

        CommandManager cm = server.getCommandManager();
        cm.register(
                cm.metaBuilder("clogs")
                        .aliases("cmdlogger", "cmdlogger", "clogs")
                        .plugin(this)
                        .build(),
                new LogsCommand(server, logger, config, opManager, permissionChecker)
        );

        logger.info("===========================================");
        logger.info("  CommandLogger v2.2.0 by muvixo");
        logger.info("  Channel: {}", config.getChannel());
        logger.info("  Visibility: only backend OPs");
        logger.info("  Debug: {}", config.isDebug());
        logger.info("===========================================");
    }

    @Subscribe
    public void onProxyShutdown(ProxyShutdownEvent event) {
        if (channel != null) {
            try { server.getChannelRegistrar().unregister(channel); } catch (Exception ignored) {}
        }
        logger.info("CommandLogger disabled.");
    }

    public Config getConfig() { return config; }
}
"""

VELOCITY_CONFIG = """package ir.muvixo.cmdlogger.velocity;

import org.slf4j.Logger;
import org.spongepowered.configurate.CommentedConfigurationNode;
import org.spongepowered.configurate.yaml.YamlConfigurationLoader;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Config manager for CommandLogger v2.2.
 *
 * @author muvixo
 */
public class Config {

    private final Path dataDirectory;
    private final Logger logger;

    private String channel;
    private String messageFormat;
    private String reloadSuccessMessage;
    private String noPermissionMessage;
    private boolean showToSelf;
    private boolean logToConsole;
    private boolean debug;
    private int opCacheExpireMinutes;
    private String seePermission;
    private String adminPermission;

    public Config(Path dataDirectory, Logger logger) {
        this.dataDirectory = dataDirectory;
        this.logger = logger;
    }

    public void load() {
        Path file = dataDirectory.resolve("config.yml");

        if (!Files.exists(file)) {
            try (InputStream in = getClass().getResourceAsStream("/config.yml")) {
                if (in != null) Files.copy(in, file);
                else Files.writeString(file, "# default config\\n");
            } catch (IOException e) {
                logger.error("Could not save default config", e);
            }
        }

        CommentedConfigurationNode root;
        try {
            root = YamlConfigurationLoader.builder().path(file).build().load();
        } catch (IOException e) {
            logger.error("Could not load config.yml", e);
            return;
        }

        this.channel = root.node("channel").getString("commandlogger:main");
        this.showToSelf = root.node("show-to-self").getBoolean(false);
        this.logToConsole = root.node("log-to-console").getBoolean(true);
        this.debug = root.node("debug").getBoolean(false);
        this.opCacheExpireMinutes = root.node("op-cache-expire-minutes").getInt(5);

        this.messageFormat = root.node("message-format").getString(
                "&8[&cLogs&8] &e{player} &8>> &b{server} &8>> &f/{command}");
        this.reloadSuccessMessage = root.node("reload-success-message").getString(
                "&a[OK] Config reloaded successfully!");
        this.noPermissionMessage = root.node("no-permission-message").getString(
                "&c[!] You don't have permission to do that!");

        this.seePermission = root.node("permissions", "see")
                .getString("commandlogger.see");
        this.adminPermission = root.node("permissions", "admin")
                .getString("commandlogger.admin");
    }

    public String getChannel() { return channel; }
    public String getMessageFormat() { return messageFormat; }
    public String getReloadSuccessMessage() { return reloadSuccessMessage; }
    public String getNoPermissionMessage() { return noPermissionMessage; }
    public boolean isShowToSelf() { return showToSelf; }
    public boolean isLogToConsole() { return logToConsole; }
    public boolean isDebug() { return debug; }
    public int getOpCacheExpireMinutes() { return opCacheExpireMinutes; }
    public String getSeePermission() { return seePermission; }
    public String getAdminPermission() { return adminPermission; }
}
"""

VELOCITY_CONFIG_YML = """# ============================================================
#  CommandLogger v2.2 - Velocity config
#  Author: muvixo
# ============================================================

# Plugin messaging channel. MUST match the Spigot/Paper side.
channel: "commandlogger:main"

# ---------------- Behaviour ----------------
# Show the command log to the player who typed it? (set true to see your own)
show-to-self: true

# Print every logged command to the proxy console.
log-to-console: true

# Verbose debug output in the proxy log. Set to false in production.
debug: false

# How long (in minutes) to keep an offline player marked as OP.
# Safety net in case an OP_STATUS=false message was lost.
# Set to 0 to disable expiration entirely (not recommended).
op-cache-expire-minutes: 5

# ---------------- Message Format ----------------
# Placeholders: {player} {server} {command} {time}
# Supports legacy (&a, &c) and hex (&#RRGGBB) colors.
message-format: "&8[&cLogs&8] &e{player} &8>> &b{server} &8>> &f/{command}"
reload-success-message: "&a[OK] Config reloaded successfully!"
no-permission-message: "&c[!] You don't have permission to do that!"

# ============================================================
#  Permission Nodes
#  A player can see the logs if ANY of the following is true:
#    1. They are OP on a backend server (auto-detected).
#    2. They have the "see" permission below.
#    3. They have the "admin" permission below.
#
#  Grant with LuckPerms (or any perm plugin):
#    /lp group staff permission set commandlogger.see   true
#    /lp group admin permission set commandlogger.admin true
# ============================================================
permissions:
  see:   "commandlogger.see"
  admin: "commandlogger.admin"
"""

VELOCITY_COLOR_UTIL = """package ir.muvixo.cmdlogger.velocity;

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.serializer.legacy.LegacyComponentSerializer;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Color utility: legacy (&a, &c) + hex (&#RRGGBB).
 *
 * @author muvixo
 */
public final class ColorUtil {

    private static final Pattern HEX_PATTERN = Pattern.compile("&#([A-Fa-f0-9]{6})");

    private ColorUtil() {}

    public static Component color(String text) {
        if (text == null) return Component.empty();
        String withHex = translateHex(text);
        return LegacyComponentSerializer.legacyAmpersand().deserialize(withHex);
    }

    private static String translateHex(String message) {
        Matcher matcher = HEX_PATTERN.matcher(message);
        StringBuffer buffer = new StringBuffer();

        while (matcher.find()) {
            String hex = matcher.group(1);
            StringBuilder replacement = new StringBuilder("\\u00a7x");
            for (char c : hex.toCharArray()) {
                replacement.append("\\u00a7").append(c);
            }
            matcher.appendReplacement(buffer, replacement.toString());
        }
        matcher.appendTail(buffer);
        return buffer.toString();
    }
}
"""

VELOCITY_OP_MANAGER = """package ir.muvixo.cmdlogger.velocity;

import com.velocitypowered.api.event.Subscribe;
import com.velocitypowered.api.event.connection.DisconnectEvent;
import com.velocitypowered.api.event.player.ServerPostConnectEvent;
import com.velocitypowered.api.proxy.ProxyServer;
import org.slf4j.Logger;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Tracks which players are OP on a backend server.
 *
 * @author muvixo
 */
public class OpPlayerManager {

    public static class OpRecord {
        public final UUID uuid;
        public volatile String name;
        public volatile String serverName;
        public volatile long lastSeen;

        public OpRecord(UUID uuid, String name, String serverName) {
            this.uuid = uuid;
            this.name = name;
            this.serverName = serverName;
            this.lastSeen = System.currentTimeMillis();
        }

        public void refresh(String serverName) {
            this.serverName = serverName;
            this.lastSeen = System.currentTimeMillis();
        }
    }

    private final ProxyServer server;
    private final Logger logger;
    private final Config config;
    private final Map<UUID, OpRecord> opPlayers = new ConcurrentHashMap<>();
    private final Map<String, UUID> nameIndex = new ConcurrentHashMap<>();

    public OpPlayerManager(ProxyServer server, Logger logger, Config config) {
        this.server = server;
        this.logger = logger;
        this.config = config;
    }

    public void markOp(UUID uuid, String playerName, String serverName) {
        if (uuid == null) return;

        OpRecord existing = opPlayers.get(uuid);
        if (existing != null) {
            if (playerName != null && !playerName.equalsIgnoreCase(existing.name)) {
                nameIndex.remove(existing.name.toLowerCase());
                nameIndex.put(playerName.toLowerCase(), uuid);
                existing.name = playerName;
            }
            existing.refresh(serverName);
            return;
        }

        OpRecord rec = new OpRecord(uuid, playerName, serverName);
        opPlayers.put(uuid, rec);
        if (playerName != null) {
            nameIndex.put(playerName.toLowerCase(), uuid);
        }
        if (logger != null) {
            logger.info("[OP-TRACK] Marked {} ({}) as OP (backend: {})",
                    playerName, uuid, serverName);
        }
    }

    public void unmarkOp(UUID uuid, String playerName) {
        if (uuid == null) return;

        OpRecord removed = opPlayers.remove(uuid);
        if (removed != null) {
            nameIndex.remove(removed.name.toLowerCase());
            if (logger != null) {
                logger.info("[OP-TRACK] Unmarked {} ({})", removed.name, uuid);
            }
        }
        if (playerName != null) {
            nameIndex.remove(playerName.toLowerCase());
        }
    }

    public boolean isOp(UUID uuid) {
        if (uuid == null) return false;
        OpRecord rec = opPlayers.get(uuid);
        if (rec == null) return false;

        int expire = config != null ? config.getOpCacheExpireMinutes() : 30;
        if (expire > 0) {
            boolean online = server.getPlayer(uuid).isPresent();
            long age = System.currentTimeMillis() - rec.lastSeen;
            if (!online && age > expire * 60_000L) {
                opPlayers.remove(uuid);
                nameIndex.remove(rec.name.toLowerCase());
                return false;
            }
        }
        return true;
    }

    public boolean isOpByName(String name) {
        if (name == null) return false;
        UUID uuid = nameIndex.get(name.toLowerCase());
        return uuid != null && isOp(uuid);
    }

    public String getOpServer(UUID uuid) {
        OpRecord rec = opPlayers.get(uuid);
        return rec == null ? null : rec.serverName;
    }

    public int getOpCount() {
        return opPlayers.size();
    }

    public Map<UUID, OpRecord> getOpPlayers() {
        return opPlayers;
    }

    @Subscribe
    public void onDisconnect(DisconnectEvent event) {
        UUID uuid = event.getPlayer().getUniqueId();
        OpRecord rec = opPlayers.get(uuid);
        if (rec != null) {
            rec.lastSeen = System.currentTimeMillis();
        }
    }

    @Subscribe
    public void onServerPostConnect(ServerPostConnectEvent event) {
        if (logger != null && config != null && config.isDebug()) {
            logger.info("[OP-TRACK] {} connected to {} (OP status: {})",
                    event.getPlayer().getUsername(),
                    event.getPlayer().getCurrentServer()
                            .map(s -> s.getServerInfo().getName()).orElse("?"),
                    isOp(event.getPlayer().getUniqueId()));
        }
    }
}
"""

VELOCITY_PERM_CHECKER = """package ir.muvixo.cmdlogger.velocity;

import com.velocitypowered.api.proxy.Player;
import org.slf4j.Logger;

/**
 * Central permission checker.
 *
 * @author muvixo
 */
public class PermissionChecker {

    private final Config config;
    private final OpPlayerManager opManager;
    private final Logger logger;

    public PermissionChecker(Config config, OpPlayerManager opManager, Logger logger) {
        this.config = config;
        this.opManager = opManager;
        this.logger = logger;
    }

    public boolean canSee(Player player) {
        if (player == null) return false;

        if (opManager.isOp(player.getUniqueId())) return true;

        String seePerm = config.getSeePermission();
        String adminPerm = config.getAdminPermission();
        if (seePerm != null && !seePerm.isEmpty() && player.hasPermission(seePerm)) return true;
        if (adminPerm != null && !adminPerm.isEmpty() && player.hasPermission(adminPerm)) return true;

        return false;
    }

    public boolean canReload(Player player) {
        if (player == null) return false;
        String adminPerm = config.getAdminPermission();
        if (adminPerm != null && !adminPerm.isEmpty() && player.hasPermission(adminPerm)) return true;
        return opManager.isOp(player.getUniqueId());
    }

    public String explain(Player player) {
        String seePerm = config.getSeePermission();
        String adminPerm = config.getAdminPermission();
        StringBuilder sb = new StringBuilder();
        sb.append("Player: ").append(player.getUsername())
          .append(" (").append(player.getUniqueId()).append(")\\n");
        sb.append("  tracked-as-op: ").append(opManager.isOp(player.getUniqueId())).append("\\n");
        sb.append("  op-server: ").append(opManager.getOpServer(player.getUniqueId())).append("\\n");
        sb.append("  has ").append(seePerm).append(": ")
          .append(player.hasPermission(seePerm)).append("\\n");
        sb.append("  has ").append(adminPerm).append(": ")
          .append(player.hasPermission(adminPerm)).append("\\n");
        sb.append("  RESULT: ").append(canSee(player) ? "CAN SEE LOGS" : "CANNOT SEE LOGS");
        return sb.toString();
    }
}
"""

VELOCITY_BACKEND_RECEIVER = """package ir.muvixo.cmdlogger.velocity;

import com.google.common.io.ByteArrayDataInput;
import com.google.common.io.ByteStreams;
import com.velocitypowered.api.event.Subscribe;
import com.velocitypowered.api.event.connection.PluginMessageEvent;
import com.velocitypowered.api.proxy.Player;
import com.velocitypowered.api.proxy.ProxyServer;
import com.velocitypowered.api.proxy.ServerConnection;
import com.velocitypowered.api.proxy.messages.MinecraftChannelIdentifier;
import net.kyori.adventure.text.Component;
import org.slf4j.Logger;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.UUID;

/**
 * Receives plugin messages from Spigot/Paper backends.
 *
 * @author muvixo
 */
public class BackendMessageReceiver {

    private static final DateTimeFormatter TIME_FORMAT = DateTimeFormatter.ofPattern("HH:mm:ss");

    private final ProxyServer server;
    private final Logger logger;
    private final Config config;
    private final OpPlayerManager opManager;
    private final PermissionChecker permChecker;
    private final MinecraftChannelIdentifier channel;

    public BackendMessageReceiver(ProxyServer server, Logger logger, Config config,
                                  OpPlayerManager opManager, PermissionChecker permChecker) {
        this.server = server;
        this.logger = logger;
        this.config = config;
        this.opManager = opManager;
        this.permChecker = permChecker;
        this.channel = MinecraftChannelIdentifier.from(config.getChannel());
    }

    @Subscribe
    public void onPluginMessage(PluginMessageEvent event) {
        if (!event.getIdentifier().equals(channel)) return;
        event.setResult(PluginMessageEvent.ForwardResult.handled());

        if (!(event.getSource() instanceof ServerConnection connection)) return;
        String sourceServer = connection.getServerInfo().getName();

        try {
            ByteArrayDataInput in = ByteStreams.newDataInput(event.getData());
            String type = in.readUTF();

            switch (type) {
                case "OP_STATUS" -> handleOpStatus(in, sourceServer);
                case "CMD"       -> handleCommand(in, sourceServer);
                default -> logger.warn("[CommandLogger] Unknown message type: {}", type);
            }
        } catch (Exception e) {
            logger.warn("[CommandLogger] Failed to decode plugin message from {}", sourceServer, e);
        }
    }

    private void handleOpStatus(ByteArrayDataInput in, String sourceServer) {
        UUID uuid = UUID.fromString(in.readUTF());
        String name = in.readUTF();
        String serverName = in.readUTF();
        boolean isOp = Boolean.parseBoolean(in.readUTF());

        if (isOp) opManager.markOp(uuid, name, serverName);
        else      opManager.unmarkOp(uuid, name);

        if (config.isDebug()) {
            logger.info("[OP-TRACK] {} -> {} (from {})", name, isOp, serverName);
        }
    }

    private void handleCommand(ByteArrayDataInput in, String sourceServer) {
        UUID uuid = UUID.fromString(in.readUTF());
        String name = in.readUTF();
        String serverName = in.readUTF();
        boolean isOp = Boolean.parseBoolean(in.readUTF());
        String command = in.readUTF();

        if (isOp) opManager.markOp(uuid, name, serverName);
        else      opManager.unmarkOp(uuid, name);

        broadcast(name, serverName, command);
    }

    private void broadcast(String playerName, String serverName, String command) {

        String time = LocalTime.now().format(TIME_FORMAT);
        String raw = config.getMessageFormat()
                .replace("{player}",  playerName)
                .replace("{server}",  serverName)
                .replace("{command}", command)
                .replace("{time}",    time);
        Component message = ColorUtil.color(raw);

        int total = 0, sent = 0;
        for (Player online : server.getAllPlayers()) {
            total++;

            if (!permChecker.canSee(online)) continue;

            if (!config.isShowToSelf()
                    && online.getUsername().equalsIgnoreCase(playerName)) {
                continue;
            }

            online.sendMessage(message);
            sent++;
        }

        if (config.isLogToConsole()) {
            logger.info("[{}@{}] /{}  (online: {}, sent: {}, tracked-ops: {})",
                    playerName, serverName, command, total, sent, opManager.getOpCount());
        }
    }
}
"""

VELOCITY_LOGS_COMMAND = """package ir.muvixo.cmdlogger.velocity;

import com.velocitypowered.api.command.CommandSource;
import com.velocitypowered.api.command.SimpleCommand;
import com.velocitypowered.api.proxy.Player;
import com.velocitypowered.api.proxy.ProxyServer;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import org.slf4j.Logger;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

/**
 * /clogs command with a permission-aware help menu.
 *
 * @author muvixo
 */
public class LogsCommand implements SimpleCommand {

    private final ProxyServer server;
    private final Logger logger;
    private final Config config;
    private final OpPlayerManager opManager;
    private final PermissionChecker permChecker;

    public LogsCommand(ProxyServer server, Logger logger, Config config,
                       OpPlayerManager opManager, PermissionChecker permChecker) {
        this.server = server;
        this.logger = logger;
        this.config = config;
        this.opManager = opManager;
        this.permChecker = permChecker;
    }

    @Override
    public void execute(Invocation invocation) {
        CommandSource source = invocation.source();
        String[] args = invocation.arguments();

        if (args.length == 0) { sendHelp(source); return; }

        String sub = args[0].toLowerCase();

        switch (sub) {
            case "help":
            case "?":
                sendHelp(source);
                return;

            case "info":
                if (!canUse(source)) { noPerm(source); return; }
                sendInfo(source);
                return;

            case "creator":
            case "author":
                if (!canUse(source)) { noPerm(source); return; }
                sendCreator(source);
                return;

            case "reload":
                if (!canReload(source)) { noPerm(source); return; }
                config.load();
                source.sendMessage(ColorUtil.color(config.getReloadSuccessMessage()));
                logger.info("Config reloaded by {}", source);
                return;

            case "list":
                if (!canReload(source)) { noPerm(source); return; }
                sendOpList(source);
                return;

            case "op": {
                if (!canReload(source)) { noPerm(source); return; }
                if (args.length < 2) {
                    source.sendMessage(Component.text("Usage: /clogs op <player>", NamedTextColor.RED));
                    return;
                }
                Optional<Player> opt = server.getPlayer(args[1]);
                if (opt.isEmpty()) {
                    source.sendMessage(Component.text("Player not found: " + args[1], NamedTextColor.RED));
                    return;
                }
                opManager.markOp(opt.get().getUniqueId(), opt.get().getUsername(), "manual");
                source.sendMessage(Component.text("Marked " + args[1] + " as OP.", NamedTextColor.GREEN));
                return;
            }

            case "unop": {
                if (!canReload(source)) { noPerm(source); return; }
                if (args.length < 2) {
                    source.sendMessage(Component.text("Usage: /clogs unop <player>", NamedTextColor.RED));
                    return;
                }
                Optional<Player> opt = server.getPlayer(args[1]);
                if (opt.isEmpty()) {
                    source.sendMessage(Component.text("Player not found: " + args[1], NamedTextColor.RED));
                    return;
                }
                opManager.unmarkOp(opt.get().getUniqueId(), opt.get().getUsername());
                source.sendMessage(Component.text("Unmarked " + args[1] + " as OP.", NamedTextColor.GREEN));
                return;
            }

            case "debug":
            case "status": {
                if (!canReload(source)) { noPerm(source); return; }
                if (args.length < 2) {
                    source.sendMessage(Component.text(
                            "Usage: /clogs " + sub + " <player>", NamedTextColor.RED));
                    return;
                }
                Optional<Player> opt = server.getPlayer(args[1]);
                if (opt.isEmpty()) {
                    source.sendMessage(Component.text(
                            "Player not found: " + args[1], NamedTextColor.RED));
                    return;
                }
                String report = permChecker.explain(opt.get());
                for (String line : report.split("\\n")) {
                    source.sendMessage(Component.text(line, NamedTextColor.GRAY));
                }
                return;
            }

            default:
                sendHelp(source);
        }
    }

    private boolean canUse(CommandSource source) {
        if (!(source instanceof Player)) return true;
        return permChecker.canSee((Player) source);
    }

    private boolean canReload(CommandSource source) {
        if (!(source instanceof Player)) return true;
        return permChecker.canReload((Player) source);
    }

    private void sendHelp(CommandSource source) {
        boolean isAdmin = canReload(source);
        boolean isUser  = canUse(source);

        if (!isAdmin && !isUser) {
            noPerm(source);
            return;
        }

        header(source, "CommandLogger - Velocity Commands");

        source.sendMessage(Component.text("General Commands", NamedTextColor.YELLOW));
        row(source, "/clogs help", "Show this help");

        if (isUser) {
            row(source, "/clogs info", "Show plugin info");
            row(source, "/clogs creator", "Show plugin credits");
        }

        if (isAdmin) {
            separator(source);
            source.sendMessage(Component.text("Admin Commands", NamedTextColor.RED));
            row(source, "/clogs reload", "Reload config");
            row(source, "/clogs list", "List tracked OPs");
            row(source, "/clogs op <player>", "Manually mark OP");
            row(source, "/clogs unop <player>", "Manually unmark OP");
            row(source, "/clogs debug <player>", "Diagnose player");
            row(source, "/clogs status <player>", "Same as debug");
        }

        separator(source);
        source.sendMessage(Component.text("Channel: ", NamedTextColor.GRAY)
                .append(Component.text(config.getChannel(), NamedTextColor.YELLOW)));
        source.sendMessage(Component.text("Tracked OPs: ", NamedTextColor.GRAY)
                .append(Component.text(String.valueOf(opManager.getOpCount()), NamedTextColor.YELLOW)));
        separator(source);
    }

    private void sendInfo(CommandSource source) {
        source.sendMessage(Component.text("CommandLogger ", NamedTextColor.GOLD)
                .append(Component.text("v2.2.0 ", NamedTextColor.YELLOW))
                .append(Component.text("by muvixo", NamedTextColor.AQUA)));
        source.sendMessage(Component.text("Channel: ", NamedTextColor.GRAY)
                .append(Component.text(config.getChannel(), NamedTextColor.WHITE)));
        source.sendMessage(Component.text("Tracked OPs: ", NamedTextColor.GRAY)
                .append(Component.text(String.valueOf(opManager.getOpCount()), NamedTextColor.WHITE)));
    }

    private void sendCreator(CommandSource source) {
        source.sendMessage(Component.text("CommandLogger ", NamedTextColor.GOLD)
                .append(Component.text("v2.2.0", NamedTextColor.YELLOW)));
        source.sendMessage(Component.text("Author: ", NamedTextColor.GRAY)
                .append(Component.text("muvixo", NamedTextColor.AQUA)));
        source.sendMessage(Component.text("API: ", NamedTextColor.GRAY)
                .append(Component.text("Velocity 3.x", NamedTextColor.WHITE)));
    }

    private void sendOpList(CommandSource source) {
        Map<UUID, OpPlayerManager.OpRecord> ops = opManager.getOpPlayers();
        header(source, "Tracked OPs (" + ops.size() + ")");

        if (ops.isEmpty()) {
            source.sendMessage(Component.text("  (none)", NamedTextColor.GRAY));
            separator(source);
            return;
        }

        long now = System.currentTimeMillis();
        for (OpPlayerManager.OpRecord r : ops.values()) {
            long ageSec = (now - r.lastSeen) / 1000;
            String line = String.format("  %s | server=%s | lastSeen=%ds ago",
                    r.name, r.serverName, ageSec);
            source.sendMessage(Component.text(line, NamedTextColor.GRAY));
        }
        separator(source);
    }

    private void header(CommandSource source, String title) {
        separator(source);
        source.sendMessage(Component.text(title, NamedTextColor.GOLD));
        separator(source);
    }

    private void separator(CommandSource source) {
        source.sendMessage(Component.text("----------------------------------",
                NamedTextColor.DARK_GRAY));
    }

    private void row(CommandSource source, String cmd, String desc) {
        source.sendMessage(Component.text("  " + cmd, NamedTextColor.GOLD)
                .append(Component.text(" - " + desc, NamedTextColor.GRAY)));
    }

    private void noPerm(CommandSource source) {
        source.sendMessage(ColorUtil.color(config.getNoPermissionMessage()));
    }

    @Override
    public boolean hasPermission(Invocation invocation) {
        return true;
    }

    @Override
    public List<String> suggest(Invocation invocation) {
        CommandSource source = invocation.source();
        String[] args = invocation.arguments();
        List<String> out = new ArrayList<>();

        if (args.length <= 1) {
            boolean isAdmin = canReload(source);
            boolean isUser  = canUse(source);

            if (!isAdmin && !isUser) return out;

            List<String> subs = new ArrayList<>();
            subs.add("help");

            if (isUser) {
                subs.add("info");
                subs.add("creator");
            }
            if (isAdmin) {
                subs.add("reload");
                subs.add("list");
                subs.add("op");
                subs.add("unop");
                subs.add("debug");
                subs.add("status");
            }

            String partial = args.length == 0 ? "" : args[0].toLowerCase();
            for (String s : subs) if (s.startsWith(partial)) out.add(s);
            return out;
        }

        if (args.length == 2) {
            String sub = args[0].toLowerCase();
            if ((sub.equals("debug") || sub.equals("status") || sub.equals("op") || sub.equals("unop"))
                    && canReload(source)) {
                String partial = args[1].toLowerCase();
                for (Player p : server.getAllPlayers()) {
                    if (p.getUsername().toLowerCase().startsWith(partial)) {
                        out.add(p.getUsername());
                    }
                }
            }
        }
        return out;
    }
}
"""

# ============================================================
#  BUNGEECORD PLUGIN
# ============================================================
BUNGEE_POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>ir.muvixo</groupId>
        <artifactId>commandlogger-parent</artifactId>
        <version>2.2.0</version>
    </parent>

    <artifactId>commandlogger-bungee</artifactId>
    <packaging>jar</packaging>
    <name>CommandLogger (BungeeCord 1.8)</name>

    <dependencies>
        <dependency>
            <groupId>net.md-5</groupId>
            <artifactId>bungeecord-api</artifactId>
            <version>1.8-SNAPSHOT</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <finalName>${project.artifactId}-${project.version}</finalName>
        <resources>
            <resource>
                <directory>src/main/resources</directory>
                <filtering>true</filtering>
                <includes>
                    <include>plugin.yml</include>
                </includes>
            </resource>
            <resource>
                <directory>src/main/resources</directory>
                <filtering>false</filtering>
                <excludes>
                    <exclude>plugin.yml</exclude>
                </excludes>
            </resource>
        </resources>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"""

BUNGEE_MAIN = """package ir.muvixo.cmdlogger.bungee;

import net.md_5.bungee.api.plugin.Plugin;
import net.md_5.bungee.api.plugin.PluginManager;
import net.md_5.bungee.api.scheduler.ScheduledTask;
import net.md_5.bungee.api.ProxyServer;

import java.util.concurrent.TimeUnit;

/**
 * CommandLogger v2.2 - Broadcasts commands from backend Spigot/Paper servers
 * to staff / OP players on the BungeeCord proxy.
 *
 * Full BungeeCord 1.8+ support.
 *
 * @author muvixo
 */
public class CommandLogger extends Plugin {

    private Config config;
    private OpPlayerManager opManager;
    private PermissionChecker permissionChecker;
    private BackendMessageReceiver receiver;
    private ScheduledTask opSyncTask;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        this.config = new Config(this);
        this.config.load();

        this.opManager = new OpPlayerManager(this, config);
        this.permissionChecker = new PermissionChecker(config, opManager, this);

        this.receiver = new BackendMessageReceiver(this, config, opManager, permissionChecker);
        getProxy().getPluginManager().registerListener(this, receiver);
        getProxy().registerChannel(config.getChannel());

        CommandLoggerCommand cmd = new CommandLoggerCommand(this, config, opManager, permissionChecker);
        getProxy().getPluginManager().registerCommand(this, cmd);

        // Periodic OP status sync (safety net)
        int interval = config.getOpStatusIntervalMinutes();
        if (interval > 0) {
            opSyncTask = getProxy().getScheduler().schedule(this, new Runnable() {
                @Override
                public void run() {
                    for (net.md_5.bungee.api.connection.ProxiedPlayer p : getProxy().getPlayers()) {
                        if (p.isConnected()) {
                            // OP status is reported by backend, but we refresh
                            // the lastSeen timestamp for online players.
                        }
                    }
                }
            }, interval, interval, TimeUnit.MINUTES);
        }

        getLogger().info("===========================================");
        getLogger().info("  CommandLogger v" + getDescription().getVersion());
        getLogger().info("  Channel: " + config.getChannel());
        getLogger().info("  Report OP: " + config.isReportOpStatus());
        getLogger().info("  Debug: " + config.isDebug());
        getLogger().info("===========================================");
    }

    @Override
    public void onDisable() {
        if (opSyncTask != null) {
            opSyncTask.cancel();
        }
        try {
            getProxy().unregisterChannel(config.getChannel());
        } catch (Exception ignored) {}
        getLogger().info("CommandLogger disabled.");
    }

    public void reloadAll() {
        config.load();
        getLogger().info("[CommandLogger] Config reloaded.");
    }

    // ============================================================
    //  GETTERS
    // ============================================================
    public Config getPluginConfig() { return config; }
    public OpPlayerManager getOpManager() { return opManager; }
    public PermissionChecker getPermissionChecker() { return permissionChecker; }
}
"""

BUNGEE_CONFIG = """package ir.muvixo.cmdlogger.bungee;

import net.md_5.bungee.config.Configuration;
import net.md_5.bungee.config.ConfigurationProvider;
import net.md_5.bungee.config.YamlConfiguration;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Config wrapper for CommandLogger v2.2.
 *
 * @author muvixo
 */
public class Config {

    private final CommandLogger plugin;

    private String channel;
    private String messageFormat;
    private String reloadSuccessMessage;
    private String noPermissionMessage;
    private boolean showToSelf;
    private boolean logToConsole;
    private boolean debug;
    private boolean reportOpStatus;
    private int opCacheExpireMinutes;
    private int opStatusIntervalMinutes;
    private String seePermission;
    private String adminPermission;

    public Config(CommandLogger plugin) {
        this.plugin = plugin;
    }

    public void load() {
        try {
            if (!plugin.getDataFolder().exists()) {
                plugin.getDataFolder().mkdirs();
            }

            File file = new File(plugin.getDataFolder(), "config.yml");
            if (!file.exists()) {
                try (InputStream in = plugin.getResourceAsStream("config.yml")) {
                    if (in != null) {
                        Files.copy(in, file.toPath());
                    }
                }
            }

            Configuration cfg = ConfigurationProvider.getProvider(YamlConfiguration.class).load(file);

            this.channel = cfg.getString("channel", "commandlogger:main");
            this.showToSelf = cfg.getBoolean("show-to-self", false);
            this.logToConsole = cfg.getBoolean("log-to-console", true);
            this.debug = cfg.getBoolean("debug", false);
            this.reportOpStatus = cfg.getBoolean("report-op-status", true);
            this.opCacheExpireMinutes = cfg.getInt("op-cache-expire-minutes", 5);
            this.opStatusIntervalMinutes = cfg.getInt("op-status-interval-minutes", 1);

            this.messageFormat = cfg.getString("message-format",
                    "&8[&cLogs&8] &e{player} &8>> &b{server} &8>> &f/{command}");
            this.reloadSuccessMessage = cfg.getString("reload-success-message",
                    "&a[OK] Config reloaded successfully!");
            this.noPermissionMessage = cfg.getString("no-permission-message",
                    "&c[!] You don't have permission to do that!");

            this.seePermission = cfg.getString("permissions.see", "commandlogger.see");
            this.adminPermission = cfg.getString("permissions.admin", "commandlogger.admin");

        } catch (IOException e) {
            plugin.getLogger().severe("Could not load config.yml: " + e.getMessage());
        }
    }

    public String getChannel() { return channel; }
    public String getMessageFormat() { return messageFormat; }
    public String getReloadSuccessMessage() { return reloadSuccessMessage; }
    public String getNoPermissionMessage() { return noPermissionMessage; }
    public boolean isShowToSelf() { return showToSelf; }
    public boolean isLogToConsole() { return logToConsole; }
    public boolean isDebug() { return debug; }
    public boolean isReportOpStatus() { return reportOpStatus; }
    public int getOpCacheExpireMinutes() { return opCacheExpireMinutes; }
    public int getOpStatusIntervalMinutes() { return opStatusIntervalMinutes; }
    public String getSeePermission() { return seePermission; }
    public String getAdminPermission() { return adminPermission; }
}
"""

BUNGEE_CONFIG_YML = """# ============================================================
#  CommandLogger v2.2 - BungeeCord config
#  Author: muvixo
# ============================================================

# Plugin messaging channel. MUST match the Spigot/Paper side.
channel: "commandlogger:main"

# ---------------- Behaviour ----------------
# Show the command log to the player who typed it?
show-to-self: true

# Print every logged command to the proxy console.
log-to-console: true

# Verbose debug output in the proxy log. Set to false in production.
debug: false

# Send OP status to the proxy on player join, quit, AND with every command?
report-op-status: true

# How long (in minutes) to keep an offline player marked as OP.
# Safety net in case an OP_STATUS=false message was lost.
# Set to 0 to disable expiration entirely (not recommended).
op-cache-expire-minutes: 5

# Also report OP status periodically as a safety net.
# Lower = faster sync, slightly more traffic. 1 is a good value.
op-status-interval-minutes: 1

# ---------------- Message Format ----------------
# Placeholders: {player} {server} {command} {time}
# Supports legacy (&a, &c) and hex (&#RRGGBB) colors.
message-format: "&8[&cLogs&8] &e{player} &8>> &b{server} &8>> &f/{command}"
reload-success-message: "&a[OK] Config reloaded successfully!"
no-permission-message: "&c[!] You don't have permission to do that!"

# ============================================================
#  Permission Nodes
#  A player can see the logs if ANY of the following is true:
#    1. They are OP on a backend server (auto-detected).
#    2. They have the "see" permission below.
#    3. They have the "admin" permission below.
#
#  Grant with LuckPerms (or any perm plugin):
#    /lp group staff permission set commandlogger.see   true
#    /lp group admin permission set commandlogger.admin true
# ============================================================
permissions:
  see:   "commandlogger.see"
  admin: "commandlogger.admin"
"""

BUNGEE_PLUGIN_YML = """name: CommandLogger
main: ir.muvixo.cmdlogger.bungee.CommandLogger
version: ${project.version}
author: muvixo
description: Forwards every command executed by players to BungeeCord staff

commands:
  logs:
    description: CommandLogger main command
    usage: /clogs help
    aliases: [vlogs, commandlogger, cmdlogs, commandlogs]
"""

BUNGEE_OP_MANAGER = """package ir.muvixo.cmdlogger.bungee;

import net.md_5.bungee.api.connection.ProxiedPlayer;
import net.md_5.bungee.api.event.PlayerDisconnectEvent;
import net.md_5.bungee.api.event.ServerConnectedEvent;
import net.md_5.bungee.api.plugin.Listener;
import net.md_5.bungee.event.EventHandler;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Tracks which players are OP on a backend server.
 *
 * @author muvixo
 */
public class OpPlayerManager implements Listener {

    public static class OpRecord {
        public final UUID uuid;
        public volatile String name;
        public volatile String serverName;
        public volatile long lastSeen;

        public OpRecord(UUID uuid, String name, String serverName) {
            this.uuid = uuid;
            this.name = name;
            this.serverName = serverName;
            this.lastSeen = System.currentTimeMillis();
        }

        public void refresh(String serverName) {
            this.serverName = serverName;
            this.lastSeen = System.currentTimeMillis();
        }
    }

    private final CommandLogger plugin;
    private final Config config;
    private final Map<UUID, OpRecord> opPlayers = new ConcurrentHashMap<UUID, OpRecord>();
    private final Map<String, UUID> nameIndex = new ConcurrentHashMap<String, UUID>();

    public OpPlayerManager(CommandLogger plugin, Config config) {
        this.plugin = plugin;
        this.config = config;
    }

    public void markOp(UUID uuid, String playerName, String serverName) {
        if (uuid == null) return;

        OpRecord existing = opPlayers.get(uuid);
        if (existing != null) {
            if (playerName != null && !playerName.equalsIgnoreCase(existing.name)) {
                nameIndex.remove(existing.name.toLowerCase());
                nameIndex.put(playerName.toLowerCase(), uuid);
                existing.name = playerName;
            }
            existing.refresh(serverName);
            return;
        }

        OpRecord rec = new OpRecord(uuid, playerName, serverName);
        opPlayers.put(uuid, rec);
        if (playerName != null) {
            nameIndex.put(playerName.toLowerCase(), uuid);
        }
        if (config.isDebug()) {
            plugin.getLogger().info("[OP-TRACK] Marked " + playerName + " (" + uuid + ") as OP (backend: " + serverName + ")");
        }
    }

    public void unmarkOp(UUID uuid, String playerName) {
        if (uuid == null) return;

        OpRecord removed = opPlayers.remove(uuid);
        if (removed != null) {
            nameIndex.remove(removed.name.toLowerCase());
            if (config.isDebug()) {
                plugin.getLogger().info("[OP-TRACK] Unmarked " + removed.name + " (" + uuid + ")");
            }
        }
        if (playerName != null) {
            nameIndex.remove(playerName.toLowerCase());
        }
    }

    public boolean isOp(UUID uuid) {
        if (uuid == null) return false;
        OpRecord rec = opPlayers.get(uuid);
        if (rec == null) return false;

        int expire = config.getOpCacheExpireMinutes();
        if (expire > 0) {
            ProxiedPlayer player = plugin.getProxy().getPlayer(uuid);
            boolean online = player != null && player.isConnected();
            long age = System.currentTimeMillis() - rec.lastSeen;
            if (!online && age > expire * 60_000L) {
                opPlayers.remove(uuid);
                nameIndex.remove(rec.name.toLowerCase());
                return false;
            }
        }
        return true;
    }

    public boolean isOpByName(String name) {
        if (name == null) return false;
        UUID uuid = nameIndex.get(name.toLowerCase());
        return uuid != null && isOp(uuid);
    }

    public String getOpServer(UUID uuid) {
        OpRecord rec = opPlayers.get(uuid);
        return rec == null ? null : rec.serverName;
    }

    public int getOpCount() {
        return opPlayers.size();
    }

    public Map<UUID, OpRecord> getOpPlayers() {
        return opPlayers;
    }

    @EventHandler
    public void onDisconnect(PlayerDisconnectEvent event) {
        UUID uuid = event.getPlayer().getUniqueId();
        OpRecord rec = opPlayers.get(uuid);
        if (rec != null) {
            rec.lastSeen = System.currentTimeMillis();
        }
    }

    @EventHandler
    public void onServerConnected(ServerConnectedEvent event) {
        if (config.isDebug()) {
            plugin.getLogger().info("[OP-TRACK] " + event.getPlayer().getName()
                    + " connected to " + event.getServer().getInfo().getName()
                    + " (OP status: " + isOp(event.getPlayer().getUniqueId()) + ")");
        }
    }
}
"""

BUNGEE_PERM_CHECKER = """package ir.muvixo.cmdlogger.bungee;

import net.md_5.bungee.api.connection.ProxiedPlayer;

/**
 * Central permission checker for BungeeCord.
 *
 * @author muvixo
 */
public class PermissionChecker {

    private final Config config;
    private final OpPlayerManager opManager;

    public PermissionChecker(Config config, OpPlayerManager opManager, CommandLogger plugin) {
        this.config = config;
        this.opManager = opManager;
    }

    public boolean canSee(ProxiedPlayer player) {
        if (player == null) return false;

        if (opManager.isOp(player.getUniqueId())) return true;

        String seePerm = config.getSeePermission();
        String adminPerm = config.getAdminPermission();
        if (seePerm != null && !seePerm.isEmpty() && player.hasPermission(seePerm)) return true;
        if (adminPerm != null && !adminPerm.isEmpty() && player.hasPermission(adminPerm)) return true;

        return false;
    }

    public boolean canReload(ProxiedPlayer player) {
        if (player == null) return false;
        String adminPerm = config.getAdminPermission();
        if (adminPerm != null && !adminPerm.isEmpty() && player.hasPermission(adminPerm)) return true;
        return opManager.isOp(player.getUniqueId());
    }

    public String explain(ProxiedPlayer player) {
        String seePerm = config.getSeePermission();
        String adminPerm = config.getAdminPermission();
        StringBuilder sb = new StringBuilder();
        sb.append("Player: ").append(player.getName())
          .append(" (").append(player.getUniqueId()).append(")\\n");
        sb.append("  tracked-as-op: ").append(opManager.isOp(player.getUniqueId())).append("\\n");
        sb.append("  op-server: ").append(opManager.getOpServer(player.getUniqueId())).append("\\n");
        sb.append("  has ").append(seePerm).append(": ")
          .append(player.hasPermission(seePerm)).append("\\n");
        sb.append("  has ").append(adminPerm).append(": ")
          .append(player.hasPermission(adminPerm)).append("\\n");
        sb.append("  RESULT: ").append(canSee(player) ? "CAN SEE LOGS" : "CANNOT SEE LOGS");
        return sb.toString();
    }
}
"""

BUNGEE_BACKEND_RECEIVER = """package ir.muvixo.cmdlogger.bungee;

import com.google.common.io.ByteArrayDataInput;
import com.google.common.io.ByteStreams;
import net.md_5.bungee.api.ChatColor;
import net.md_5.bungee.api.chat.TextComponent;
import net.md_5.bungee.api.connection.ProxiedPlayer;
import net.md_5.bungee.api.connection.Server;
import net.md_5.bungee.api.event.PluginMessageEvent;
import net.md_5.bungee.api.plugin.Listener;
import net.md_5.bungee.event.EventHandler;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.UUID;

/**
 * Receives plugin messages from Spigot/Paper backends on BungeeCord.
 *
 * @author muvixo
 */
public class BackendMessageReceiver implements Listener {

    private static final DateTimeFormatter TIME_FORMAT = DateTimeFormatter.ofPattern("HH:mm:ss");

    private final CommandLogger plugin;
    private final Config config;
    private final OpPlayerManager opManager;
    private final PermissionChecker permChecker;

    public BackendMessageReceiver(CommandLogger plugin, Config config,
                                  OpPlayerManager opManager, PermissionChecker permChecker) {
        this.plugin = plugin;
        this.config = config;
        this.opManager = opManager;
        this.permChecker = permChecker;
    }

    @EventHandler
    public void onPluginMessage(PluginMessageEvent event) {
        if (!event.getTag().equalsIgnoreCase(config.getChannel())) return;

        event.setCancelled(true);

        if (!(event.getSender() instanceof Server)) return;
        Server server = (Server) event.getSender();
        String sourceServer = server.getInfo().getName();

        try {
            ByteArrayDataInput in = ByteStreams.newDataInput(event.getData());
            String type = in.readUTF();

            if ("OP_STATUS".equals(type)) {
                handleOpStatus(in, sourceServer);
            } else if ("CMD".equals(type)) {
                handleCommand(in, sourceServer);
            } else {
                plugin.getLogger().warning("[CommandLogger] Unknown message type: " + type);
            }
        } catch (Exception e) {
            plugin.getLogger().warning("[CommandLogger] Failed to decode plugin message from "
                    + sourceServer + ": " + e.getMessage());
        }
    }

    private void handleOpStatus(ByteArrayDataInput in, String sourceServer) {
        UUID uuid = UUID.fromString(in.readUTF());
        String name = in.readUTF();
        String serverName = in.readUTF();
        boolean isOp = Boolean.parseBoolean(in.readUTF());

        if (isOp) opManager.markOp(uuid, name, serverName);
        else      opManager.unmarkOp(uuid, name);

        if (config.isDebug()) {
            plugin.getLogger().info("[OP-TRACK] " + name + " -> " + isOp + " (from " + serverName + ")");
        }
    }

    private void handleCommand(ByteArrayDataInput in, String sourceServer) {
        UUID uuid = UUID.fromString(in.readUTF());
        String name = in.readUTF();
        String serverName = in.readUTF();
        boolean isOp = Boolean.parseBoolean(in.readUTF());
        String command = in.readUTF();

        if (isOp) opManager.markOp(uuid, name, serverName);
        else      opManager.unmarkOp(uuid, name);

        broadcast(name, serverName, command);
    }

    private void broadcast(String playerName, String serverName, String command) {

        String time = LocalTime.now().format(TIME_FORMAT);
        String raw = config.getMessageFormat()
                .replace("{player}",  playerName)
                .replace("{server}",  serverName)
                .replace("{command}", command)
                .replace("{time}",    time);
        TextComponent message = new TextComponent(
                ChatColor.translateAlternateColorCodes('&', raw));

        int total = 0, sent = 0;
        for (ProxiedPlayer online : plugin.getProxy().getPlayers()) {
            total++;

            if (!permChecker.canSee(online)) continue;

            if (!config.isShowToSelf()
                    && online.getName().equalsIgnoreCase(playerName)) {
                continue;
            }

            online.sendMessage(message);
            sent++;
        }

        if (config.isLogToConsole()) {
            plugin.getLogger().info("[" + playerName + "@" + serverName + "] /"
                    + command + "  (online: " + total + ", sent: " + sent
                    + ", tracked-ops: " + opManager.getOpCount() + ")");
        }
    }
}
"""

BUNGEE_LOGS_COMMAND = """package ir.muvixo.cmdlogger.bungee;

import net.md_5.bungee.api.ChatColor;
import net.md_5.bungee.api.CommandSender;
import net.md_5.bungee.api.chat.TextComponent;
import net.md_5.bungee.api.connection.ProxiedPlayer;
import net.md_5.bungee.api.plugin.Command;
import net.md_5.bungee.api.plugin.TabExecutor;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * /clogs command for BungeeCord with a permission-aware help menu.
 *
 * @author muvixo
 */
public class CommandLoggerCommand extends Command implements TabExecutor {

    private final CommandLogger plugin;
    private final Config config;
    private final OpPlayerManager opManager;
    private final PermissionChecker permChecker;

    public CommandLoggerCommand(CommandLogger plugin, Config config,
                             OpPlayerManager opManager, PermissionChecker permChecker) {
        super("clogs", null, "clogs", "commandlogger", "cmdlogger", "cmdlogger");
        this.plugin = plugin;
        this.config = config;
        this.opManager = opManager;
        this.permChecker = permChecker;
    }

    @Override
    public void execute(CommandSender sender, String[] args) {
        if (args.length == 0) { sendHelp(sender); return; }

        String sub = args[0].toLowerCase();

        if (sub.equals("help") || sub.equals("?")) {
            sendHelp(sender);
            return;
        }

        if (sub.equals("info")) {
            if (!canUse(sender)) { noPerm(sender); return; }
            sendInfo(sender);
            return;
        }

        if (sub.equals("creator") || sub.equals("author")) {
            if (!canUse(sender)) { noPerm(sender); return; }
            sendCreator(sender);
            return;
        }

        if (sub.equals("reload")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            plugin.reloadAll();
            sender.sendMessage(new TextComponent(ChatColor.translateAlternateColorCodes('&',
                    config.getReloadSuccessMessage())));
            return;
        }

        if (sub.equals("list")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            sendOpList(sender);
            return;
        }

        if (sub.equals("op")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            if (args.length < 2) {
                sender.sendMessage(new TextComponent(ChatColor.RED + "Usage: /clogs op <player>"));
                return;
            }
            ProxiedPlayer target = plugin.getProxy().getPlayer(args[1]);
            if (target == null) {
                sender.sendMessage(new TextComponent(ChatColor.RED + "Player not found: " + args[1]));
                return;
            }
            opManager.markOp(target.getUniqueId(), target.getName(), "manual");
            sender.sendMessage(new TextComponent(ChatColor.GREEN + "Marked " + args[1] + " as OP."));
            return;
        }

        if (sub.equals("unop")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            if (args.length < 2) {
                sender.sendMessage(new TextComponent(ChatColor.RED + "Usage: /clogs unop <player>"));
                return;
            }
            ProxiedPlayer target = plugin.getProxy().getPlayer(args[1]);
            if (target == null) {
                sender.sendMessage(new TextComponent(ChatColor.RED + "Player not found: " + args[1]));
                return;
            }
            opManager.unmarkOp(target.getUniqueId(), target.getName());
            sender.sendMessage(new TextComponent(ChatColor.GREEN + "Unmarked " + args[1] + " as OP."));
            return;
        }

        if (sub.equals("debug") || sub.equals("status")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            if (args.length < 2) {
                sender.sendMessage(new TextComponent(ChatColor.RED
                        + "Usage: /clogs " + sub + " <player>"));
                return;
            }
            ProxiedPlayer target = plugin.getProxy().getPlayer(args[1]);
            if (target == null) {
                sender.sendMessage(new TextComponent(ChatColor.RED
                        + "Player not found: " + args[1]));
                return;
            }
            String report = permChecker.explain(target);
            for (String line : report.split("\\n")) {
                sender.sendMessage(new TextComponent(ChatColor.GRAY + line));
            }
            return;
        }

        sendHelp(sender);
    }

    private boolean canUse(CommandSender sender) {
        if (!(sender instanceof ProxiedPlayer)) return true;
        return permChecker.canSee((ProxiedPlayer) sender);
    }

    private boolean canReload(CommandSender sender) {
        if (!(sender instanceof ProxiedPlayer)) return true;
        return permChecker.canReload((ProxiedPlayer) sender);
    }

    private void sendHelp(CommandSender sender) {
        boolean isAdmin = canReload(sender);
        boolean isUser  = canUse(sender);

        if (!isAdmin && !isUser) {
            noPerm(sender);
            return;
        }

        header(sender, "CommandLogger - BungeeCord Commands");

        sender.sendMessage(new TextComponent(ChatColor.YELLOW + "General Commands"));
        row(sender, "/clogs help", "Show this help");

        if (isUser) {
            row(sender, "/clogs info", "Show plugin info");
            row(sender, "/clogs creator", "Show plugin credits");
        }

        if (isAdmin) {
            separator(sender);
            sender.sendMessage(new TextComponent(ChatColor.RED + "Admin Commands"));
            row(sender, "/clogs reload", "Reload config");
            row(sender, "/clogs list", "List tracked OPs");
            row(sender, "/clogs op <player>", "Manually mark OP");
            row(sender, "/clogs unop <player>", "Manually unmark OP");
            row(sender, "/clogs debug <player>", "Diagnose player");
            row(sender, "/clogs status <player>", "Same as debug");
        }

        separator(sender);
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "Channel: "
                + ChatColor.YELLOW + config.getChannel()));
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "Tracked OPs: "
                + ChatColor.YELLOW + opManager.getOpCount()));
        separator(sender);
    }

    private void sendInfo(CommandSender sender) {
        sender.sendMessage(new TextComponent(ChatColor.GOLD + "CommandLogger "
                + ChatColor.YELLOW + "v" + plugin.getDescription().getVersion()
                + ChatColor.AQUA + " by muvixo"));
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "Channel: "
                + ChatColor.WHITE + config.getChannel()));
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "Tracked OPs: "
                + ChatColor.WHITE + opManager.getOpCount()));
    }

    private void sendCreator(CommandSender sender) {
        sender.sendMessage(new TextComponent(ChatColor.GOLD + "CommandLogger "
                + ChatColor.YELLOW + "v" + plugin.getDescription().getVersion()));
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "Author: "
                + ChatColor.AQUA + "muvixo"));
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "API: "
                + ChatColor.WHITE + "BungeeCord 1.8+"));
    }

    private void sendOpList(CommandSender sender) {
        Map<UUID, OpPlayerManager.OpRecord> ops = opManager.getOpPlayers();
        header(sender, "Tracked OPs (" + ops.size() + ")");

        if (ops.isEmpty()) {
            sender.sendMessage(new TextComponent(ChatColor.GRAY + "  (none)"));
            separator(sender);
            return;
        }

        long now = System.currentTimeMillis();
        for (OpPlayerManager.OpRecord r : ops.values()) {
            long ageSec = (now - r.lastSeen) / 1000;
            String line = String.format("  %s | server=%s | lastSeen=%ds ago",
                    r.name, r.serverName, ageSec);
            sender.sendMessage(new TextComponent(ChatColor.GRAY + line));
        }
        separator(sender);
    }

    private void header(CommandSender sender, String title) {
        separator(sender);
        sender.sendMessage(new TextComponent(ChatColor.GOLD + title));
        separator(sender);
    }

    private void separator(CommandSender sender) {
        sender.sendMessage(new TextComponent(ChatColor.DARK_GRAY
                + "----------------------------------"));
    }

    private void row(CommandSender sender, String cmd, String desc) {
        sender.sendMessage(new TextComponent(ChatColor.GOLD + "  " + cmd
                + ChatColor.GRAY + " - " + desc));
    }

    private void noPerm(CommandSender sender) {
        sender.sendMessage(new TextComponent(ChatColor.translateAlternateColorCodes('&',
                config.getNoPermissionMessage())));
    }

    @Override
    public Iterable<String> onTabComplete(CommandSender sender, String[] args) {
        List<String> out = new ArrayList<String>();

        if (args.length <= 1) {
            boolean isAdmin = canReload(sender);
            boolean isUser  = canUse(sender);

            if (!isAdmin && !isUser) return out;

            List<String> subs = new ArrayList<String>();
            subs.add("help");

            if (isUser) {
                subs.add("info");
                subs.add("creator");
            }
            if (isAdmin) {
                subs.add("reload");
                subs.add("list");
                subs.add("op");
                subs.add("unop");
                subs.add("debug");
                subs.add("status");
            }

            String partial = args.length == 0 ? "" : args[0].toLowerCase();
            for (String s : subs) if (s.startsWith(partial)) out.add(s);
            return out;
        }

        if (args.length == 2) {
            String sub = args[0].toLowerCase();
            if ((sub.equals("debug") || sub.equals("status")
                    || sub.equals("op") || sub.equals("unop"))
                    && canReload(sender)) {
                String partial = args[1].toLowerCase();
                for (ProxiedPlayer p : plugin.getProxy().getPlayers()) {
                    if (p.getName().toLowerCase().startsWith(partial)) {
                        out.add(p.getName());
                    }
                }
            }
        }
        return out;
    }
}
"""

# ============================================================
#  SPIGOT PLUGIN (same as original but updated version)
# ============================================================
SPIGOT_POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>ir.muvixo</groupId>
        <artifactId>commandlogger-parent</artifactId>
        <version>2.2.0</version>
    </parent>

    <artifactId>commandlogger-spigot</artifactId>
    <packaging>jar</packaging>
    <name>CommandLogger (Spigot 1.8)</name>

    <dependencies>
        <dependency>
            <groupId>org.spigotmc</groupId>
            <artifactId>spigot-api</artifactId>
            <version>1.8.8-R0.1-SNAPSHOT</version>
            <scope>provided</scope>
            <exclusions>
                <exclusion>
                    <groupId>net.md-5</groupId>
                    <artifactId>bungeecord-chat</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>

    <build>
        <finalName>${project.artifactId}-${project.version}</finalName>
        <resources>
            <resource>
                <directory>src/main/resources</directory>
                <filtering>true</filtering>
                <includes>
                    <include>plugin.yml</include>
                </includes>
            </resource>
            <resource>
                <directory>src/main/resources</directory>
                <filtering>false</filtering>
                <excludes>
                    <exclude>plugin.yml</exclude>
                </excludes>
            </resource>
        </resources>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"""

SPIGOT_MAIN = """package ir.muvixo.cmdlogger.spigot;

import com.google.common.io.ByteArrayDataOutput;
import com.google.common.io.ByteStreams;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;

/**
 * CommandLogger v2.2 - forwards every command to the proxy.
 * Works on Minecraft 1.8.8 / 1.8.9.
 *
 * @author muvixo
 */
public class CommandLogger extends JavaPlugin {

    private Config config;

    private boolean forwardingEnabled = true;
    private boolean debugEnabled = false;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        this.config = new Config(this);
        this.config.load();

        getServer().getMessenger().registerOutgoingPluginChannel(this, config.getChannel());
        getServer().getPluginManager().registerEvents(new CommandInterceptor(this, config), this);

        VLogsCommand cmd = new VLogsCommand(this, config);
        if (getCommand("clogs") != null) {
            getCommand("clogs").setExecutor(cmd);
            getCommand("clogs").setTabCompleter(cmd);
        }

        long intervalTicks = config.getOpStatusIntervalMinutes() * 60L * 20L;
        if (intervalTicks > 0) {
            getServer().getScheduler().runTaskTimer(this, new Runnable() {
                @Override
                public void run() {
                    for (Player p : getServer().getOnlinePlayers()) {
                        if (p.isOp()) sendOpStatus(p, true);
                    }
                }
            }, intervalTicks, intervalTicks);
        }

        getLogger().info("===========================================");
        getLogger().info("  CommandLogger-Spigot v" + getDescription().getVersion());
        getLogger().info("  Channel: " + config.getChannel());
        getLogger().info("  Server name: " + config.getServerName());
        getLogger().info("  Report OP: " + config.isReportOpStatus());
        getLogger().info("===========================================");
    }

    @Override
    public void onDisable() {
        try {
            getServer().getMessenger().unregisterOutgoingPluginChannel(this);
        } catch (Exception ignored) {}
        getLogger().info("CommandLogger-Spigot disabled.");
    }

    public void reloadAll() {
        reloadConfig();
        this.config.load();
        getLogger().info("[CommandLogger] Config reloaded.");
    }

    public void sendOpStatus(Player player, boolean isOp) {
        try {
            ByteArrayDataOutput out = ByteStreams.newDataOutput();
            out.writeUTF("OP_STATUS");
            out.writeUTF(player.getUniqueId().toString());
            out.writeUTF(player.getName());
            out.writeUTF(config.getServerName());
            out.writeUTF(Boolean.toString(isOp));
            player.sendPluginMessage(this, config.getChannel(), out.toByteArray());
        } catch (Exception e) {
            getLogger().warning("Failed to send OP_STATUS: " + e.getMessage());
        }
    }

    public Config getPluginConfig()               { return config; }
    public boolean isForwardingEnabled()          { return forwardingEnabled; }
    public void setForwardingEnabled(boolean v)   { this.forwardingEnabled = v; }
    public boolean isDebugEnabled()               { return debugEnabled; }
    public void setDebugEnabled(boolean v)        { this.debugEnabled = v; }
}
"""

SPIGOT_CONFIG = """package ir.muvixo.cmdlogger.spigot;

import org.bukkit.configuration.file.FileConfiguration;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;

/**
 * Config wrapper for CommandLogger v2.2.
 *
 * @author muvixo
 */
public class Config {

    private final CommandLogger plugin;

    private String channel;
    private String serverName;
    private boolean logOps;
    private boolean reportOpStatus;
    private int opStatusIntervalMinutes;
    private List<String> blacklist;
    private List<String> ignoredPlayers;

    public Config(CommandLogger plugin) {
        this.plugin = plugin;
    }

    public void load() {
        plugin.reloadConfig();
        FileConfiguration cfg = plugin.getConfig();

        this.channel = cfg.getString("channel", "commandlogger:main");
        this.logOps = cfg.getBoolean("log-ops", true);
        this.reportOpStatus = cfg.getBoolean("report-op-status", true);
        this.opStatusIntervalMinutes = cfg.getInt("op-status-interval-minutes", 5);

        String configured = cfg.getString("server-name", "");
        if (configured != null && !configured.trim().isEmpty()) {
            this.serverName = configured.trim();
        } else {
            String bukkit = plugin.getServer().getServerName();
            if (bukkit == null || bukkit.isEmpty()
                    || bukkit.equalsIgnoreCase("Unknown Server")) {
                this.serverName = "server-" + plugin.getServer().getPort();
            } else {
                this.serverName = bukkit;
            }
        }

        List<String> rawBlacklist = cfg.getStringList("blacklist");
        if (rawBlacklist == null) rawBlacklist = new ArrayList<String>();
        this.blacklist = rawBlacklist.stream()
                .filter(s -> s != null)
                .map(s -> s.toLowerCase(Locale.ROOT).trim())
                .collect(Collectors.toList());

        List<String> rawIgnored = cfg.getStringList("ignored-players");
        if (rawIgnored == null) rawIgnored = new ArrayList<String>();
        this.ignoredPlayers = rawIgnored.stream()
                .filter(s -> s != null)
                .map(s -> s.toLowerCase(Locale.ROOT).trim())
                .collect(Collectors.toList());
    }

    public String getChannel() { return channel; }
    public String getServerName() { return serverName; }
    public boolean isLogOps() { return logOps; }
    public boolean isReportOpStatus() { return reportOpStatus; }
    public int getOpStatusIntervalMinutes() { return opStatusIntervalMinutes; }

    public boolean isBlacklisted(String command) {
        String base = command.split(" ", 2)[0].toLowerCase(Locale.ROOT);
        return blacklist.contains(base);
    }

    public boolean isIgnoredPlayer(String playerName) {
        return ignoredPlayers.contains(playerName.toLowerCase(Locale.ROOT));
    }
}
"""

SPIGOT_INTERCEPTOR = """package ir.muvixo.cmdlogger.spigot;

import com.google.common.io.ByteArrayDataOutput;
import com.google.common.io.ByteStreams;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerCommandPreprocessEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;

/**
 * Intercepts EVERY command a player types and forwards them to the proxy.
 *
 * @author muvixo
 */
public class CommandInterceptor implements Listener {

    private final CommandLogger plugin;
    private final Config config;

    public CommandInterceptor(CommandLogger plugin, Config config) {
        this.plugin = plugin;
        this.config = config;
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onJoin(PlayerJoinEvent event) {
        if (!config.isReportOpStatus()) return;
        final Player player = event.getPlayer();
        plugin.getServer().getScheduler().runTaskLater(plugin, new Runnable() {
            @Override
            public void run() {
                if (player.isOnline()) {
                    plugin.sendOpStatus(player, player.isOp());
                }
            }
        }, 20L);
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onQuit(PlayerQuitEvent event) {
        if (!config.isReportOpStatus()) return;
        plugin.sendOpStatus(event.getPlayer(), false);
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = false)
    public void onCommand(PlayerCommandPreprocessEvent event) {

        if (!plugin.isForwardingEnabled()) return;

        Player player = event.getPlayer();

        if (config.isReportOpStatus()) {
            plugin.sendOpStatus(player, player.isOp());
        }

        if (!config.isLogOps() && player.isOp()) return;
        if (config.isIgnoredPlayer(player.getName())) return;

        String full = event.getMessage();
        if (full == null || full.isEmpty()) return;

        if (full.charAt(0) != '/') return;

        String command = full.substring(1).trim();
        if (command.isEmpty()) return;

        String base = command.split(" ", 2)[0].toLowerCase();
        if (base.equals("clogs") || base.equals("clog") || base.equals("commandlogger")) return;

        if (config.isBlacklisted(command)) return;

        try {
            ByteArrayDataOutput out = ByteStreams.newDataOutput();
            out.writeUTF("CMD");
            out.writeUTF(player.getUniqueId().toString());
            out.writeUTF(player.getName());
            out.writeUTF(config.getServerName());
            out.writeUTF(Boolean.toString(player.isOp()));
            out.writeUTF(command);
            player.sendPluginMessage(plugin, config.getChannel(), out.toByteArray());

            if (plugin.isDebugEnabled()) {
                plugin.getLogger().info("[DEBUG] Forwarded: " + player.getName()
                        + " (op=" + player.isOp() + ") -> /" + command);
            }
        } catch (Exception e) {
            plugin.getLogger().warning("Failed to forward command: " + e.getMessage());
        }
    }
}
"""

SPIGOT_VLOGS_CMD = """package ir.muvixo.cmdlogger.spigot;

import java.util.ArrayList;
import java.util.List;

import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;

/**
 * /clogs - Spigot side command with a permission-aware help menu.
 *
 * @author muvixo
 */
public class VLogsCommand implements CommandExecutor, TabCompleter {

    private final CommandLogger plugin;
    private final Config config;

    public VLogsCommand(CommandLogger plugin, Config config) {
        this.plugin = plugin;
        this.config = config;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command,
                             String label, String[] args) {

        if (args.length == 0) {
            sendHelp(sender);
            return true;
        }

        String sub = args[0].toLowerCase();

        if (sub.equals("help") || sub.equals("?")) {
            sendHelp(sender);
            return true;
        }

        if (sub.equals("creator") || sub.equals("author")) {
            if (!sender.hasPermission(getPerm("creator", "commandlogger.creator"))) {
                noPerm(sender); return true;
            }
            sendCreator(sender);
            return true;
        }

        if (sub.equals("info")) {
            if (!sender.hasPermission(getPerm("use", "commandlogger.use"))) {
                noPerm(sender); return true;
            }
            sendInfo(sender);
            return true;
        }

        if (sub.equals("status")) {
            if (!sender.hasPermission(getPerm("status", "commandlogger.status"))) {
                noPerm(sender); return true;
            }
            sendStatus(sender);
            return true;
        }

        if (sub.equals("reload")) {
            if (!sender.hasPermission(getPerm("reload", "commandlogger.reload"))) {
                noPerm(sender); return true;
            }
            plugin.reloadAll();
            sender.sendMessage(colorize("&a[OK] Config reloaded."));
            return true;
        }

        if (sub.equals("toggle")) {
            if (!sender.hasPermission(getPerm("toggle", "commandlogger.toggle"))) {
                noPerm(sender); return true;
            }
            boolean now = !plugin.isForwardingEnabled();
            plugin.setForwardingEnabled(now);
            sender.sendMessage(colorize(now
                    ? "&aCommand forwarding &lENABLED&a."
                    : "&cCommand forwarding &lDISABLED&c."));
            return true;
        }

        if (sub.equals("debug")) {
            if (!sender.hasPermission(getPerm("debug", "commandlogger.debug"))) {
                noPerm(sender); return true;
            }
            boolean now = !plugin.isDebugEnabled();
            plugin.setDebugEnabled(now);
            sender.sendMessage(colorize(now
                    ? "&aDebug mode &lENABLED&a."
                    : "&cDebug mode &lDISABLED&c."));
            return true;
        }

        sender.sendMessage(colorize("&cUnknown subcommand. Use &e/clogs help"));
        return true;
    }

    private String getPerm(String action, String defaultPerm) {
        String value = plugin.getConfig().getString("permissions." + action);
        if (value == null || value.trim().isEmpty()) {
            return defaultPerm;
        }
        return value.trim();
    }

    private void sendHelp(CommandSender sender) {
        String permUse     = getPerm("use",     "commandlogger.use");
        String permCreator = getPerm("creator", "commandlogger.creator");
        String permAdmin   = getPerm("admin",   "commandlogger.admin");
        String permReload  = getPerm("reload",  "commandlogger.reload");
        String permStatus  = getPerm("status",  "commandlogger.status");
        String permToggle  = getPerm("toggle",  "commandlogger.toggle");
        String permDebug   = getPerm("debug",   "commandlogger.debug");

        boolean isAdmin =
                sender.hasPermission(permAdmin)
             || sender.hasPermission(permReload)
             || sender.hasPermission(permStatus)
             || sender.hasPermission(permToggle)
             || sender.hasPermission(permDebug);

        boolean isUser =
                sender.hasPermission(permUse)
             || sender.hasPermission(permCreator);

        if (!isAdmin && !isUser) {
            noPerm(sender);
            return;
        }

        sender.sendMessage(colorize("&8&m----------------------------------"));
        sender.sendMessage(colorize("&6&lCommandLogger &7- &eSpigot Commands"));
        sender.sendMessage(colorize("&8&m----------------------------------"));

        sender.sendMessage(colorize("&e&lGeneral Commands"));
        sender.sendMessage(colorize("  &6/clogs help &8- &7Show this help"));

        if (sender.hasPermission(permCreator)) {
            sender.sendMessage(colorize("  &6/clogs creator &8- &7Show plugin credits"));
        }
        if (sender.hasPermission(permUse)) {
            sender.sendMessage(colorize("  &6/clogs info &8- &7Show plugin info"));
        }

        if (isAdmin) {
            sender.sendMessage(colorize("&8&m----------------------------------"));
            sender.sendMessage(colorize("&c&lAdmin Commands"));

            if (sender.hasPermission(permStatus)) {
                sender.sendMessage(colorize("  &6/clogs status &8- &7Show plugin status"));
            }
            if (sender.hasPermission(permToggle)) {
                sender.sendMessage(colorize("  &6/clogs toggle &8- &7Toggle command forwarding"));
            }
            if (sender.hasPermission(permDebug)) {
                sender.sendMessage(colorize("  &6/clogs debug &8- &7Toggle debug mode"));
            }
            if (sender.hasPermission(permReload)) {
                sender.sendMessage(colorize("  &6/clogs reload &8- &7Reload configuration"));
            }
        }

        sender.sendMessage(colorize("&8&m----------------------------------"));
        sender.sendMessage(colorize("&7Channel: &e" + config.getChannel()
                + " &8| &7Server: &e" + config.getServerName()));
        sender.sendMessage(colorize("&8&m----------------------------------"));
    }

    private void sendCreator(CommandSender sender) {
        sender.sendMessage(colorize("&8&m----------------------------------"));
        sender.sendMessage(colorize("&6&lCommandLogger-Spigot"));
        sender.sendMessage(colorize("&7Author: &bmuvixo"));
        sender.sendMessage(colorize("&7Version: &f" + plugin.getDescription().getVersion()));
        sender.sendMessage(colorize("&7API: &fSpigot 1.8.8"));
        sender.sendMessage(colorize("&8&m----------------------------------"));
    }

    private void sendInfo(CommandSender sender) {
        sender.sendMessage(colorize("&8&m----------------------------------"));
        sender.sendMessage(colorize("&6&lCommandLogger &7- &eInfo"));
        sender.sendMessage(colorize("&7Channel: &e" + config.getChannel()));
        sender.sendMessage(colorize("&7Server name: &e" + config.getServerName()));
        sender.sendMessage(colorize("&7Log OPs: &e" + config.isLogOps()));
        sender.sendMessage(colorize("&7Report OP status: &e" + config.isReportOpStatus()));
        sender.sendMessage(colorize("&8&m----------------------------------"));
    }

    private void sendStatus(CommandSender sender) {
        sender.sendMessage(colorize("&8&m----------------------------------"));
        sender.sendMessage(colorize("&6&lCommandLogger &7- &eStatus"));
        sender.sendMessage(colorize("&7Forwarding: "
                + (plugin.isForwardingEnabled() ? "&aENABLED" : "&cDISABLED")));
        sender.sendMessage(colorize("&7Debug: "
                + (plugin.isDebugEnabled() ? "&aON" : "&cOFF")));
        sender.sendMessage(colorize("&7Channel: &e" + config.getChannel()));
        sender.sendMessage(colorize("&7Server name: &e" + config.getServerName()));
        sender.sendMessage(colorize("&7Log OPs: &e" + config.isLogOps()));
        sender.sendMessage(colorize("&8&m----------------------------------"));
    }

    private void noPerm(CommandSender sender) {
        sender.sendMessage(colorize("&cYou do not have permission."));
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command,
                                      String alias, String[] args) {
        List<String> out = new ArrayList<String>();

        if (args.length == 1) {
            List<String> subs = new ArrayList<String>();

            boolean isAdmin =
                    sender.hasPermission(getPerm("admin",  "commandlogger.admin"))
                 || sender.hasPermission(getPerm("reload", "commandlogger.reload"))
                 || sender.hasPermission(getPerm("status", "commandlogger.status"))
                 || sender.hasPermission(getPerm("toggle", "commandlogger.toggle"))
                 || sender.hasPermission(getPerm("debug",  "commandlogger.debug"));

            boolean isUser =
                    sender.hasPermission(getPerm("use",     "commandlogger.use"))
                 || sender.hasPermission(getPerm("creator", "commandlogger.creator"));

            if (!isAdmin && !isUser) {
                return out;
            }

            subs.add("help");

            if (sender.hasPermission(getPerm("creator", "commandlogger.creator"))) subs.add("creator");
            if (sender.hasPermission(getPerm("use",     "commandlogger.use")))     subs.add("info");
            if (sender.hasPermission(getPerm("status",  "commandlogger.status")))  subs.add("status");
            if (sender.hasPermission(getPerm("toggle",  "commandlogger.toggle")))  subs.add("toggle");
            if (sender.hasPermission(getPerm("debug",   "commandlogger.debug")))   subs.add("debug");
            if (sender.hasPermission(getPerm("reload",  "commandlogger.reload")))  subs.add("reload");

            String partial = args[0].toLowerCase();
            for (String s : subs) if (s.startsWith(partial)) out.add(s);
        }
        return out;
    }

    private String colorize(String message) {
        if (message == null) return "";
        return ChatColor.translateAlternateColorCodes('&', message);
    }
}
"""

SPIGOT_CONFIG_YML = """# ============================================================
#  CommandLogger-Spigot v2.2 - backend config
#  Author: muvixo
# ============================================================

# Plugin messaging channel. MUST match the proxy side.
channel: "commandlogger:main"

# Name of this backend server.
# Leave empty to auto-detect.
server-name: ""

# Send commands to the proxy even for OP players?
log-ops: true

# Send OP status to the proxy on player join, quit, AND with every command?
report-op-status: true

# Also report OP status periodically as a safety net.
op-status-interval-minutes: 1

# Hide these commands from being forwarded.
blacklist:
  - "login"
  - "register"
  - "changepassword"

# Ignore commands from these players entirely.
ignored-players: []

# ============================================================
#  Permission Nodes
# ============================================================
permissions:
  use:      "commandlogger.use"
  creator:  "commandlogger.creator"

  admin:    "commandlogger.admin"
  reload:   "commandlogger.reload"
  status:   "commandlogger.status"
  toggle:   "commandlogger.toggle"
  debug:    "commandlogger.debug"
"""

SPIGOT_PLUGIN_YML = """name: CommandLogger-Spigot
main: ir.muvixo.cmdlogger.spigot.CommandLogger
version: ${project.version}
author: muvixo
description: Forwards every command executed by players to the proxy

commands:
  vlogs:
    description: CommandLogger Spigot helper command
    usage: /clogs help
    aliases: [velogs, commandlogger]

permissions:
  commandlogger.use:
    description: Access to /clogs info
    default: op
  commandlogger.creator:
    description: See plugin credits
    default: op
  commandlogger.admin:
    description: Full admin access
    default: op
  commandlogger.reload:
    description: Reload config
    default: op
  commandlogger.status:
    description: Show plugin status
    default: op
  commandlogger.toggle:
    description: Toggle command forwarding on/off
    default: op
  commandlogger.debug:
    description: Toggle debug mode
    default: op
"""

# ============================================================
#  PAPER PLUGIN
# ============================================================
PAPER_POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>ir.muvixo</groupId>
        <artifactId>commandlogger-parent</artifactId>
        <version>2.2.0</version>
    </parent>

    <artifactId>commandlogger-paper</artifactId>
    <packaging>jar</packaging>
    <name>CommandLogger (Paper 1.8+)</name>

    <dependencies>
        <dependency>
            <groupId>com.destroystokyo.paper</groupId>
            <artifactId>paper-api</artifactId>
            <version>1.8.8-R0.1-SNAPSHOT</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <finalName>${project.artifactId}-${project.version}</finalName>
        <resources>
            <resource>
                <directory>src/main/resources</directory>
                <filtering>true</filtering>
                <includes>
                    <include>plugin.yml</include>
                </includes>
            </resource>
            <resource>
                <directory>src/main/resources</directory>
                <filtering>false</filtering>
                <excludes>
                    <exclude>plugin.yml</exclude>
                </excludes>
            </resource>
        </resources>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"""

PAPER_MAIN = """package ir.muvixo.cmdlogger.paper;

import com.google.common.io.ByteArrayDataOutput;
import com.google.common.io.ByteStreams;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;

/**
 * CommandLogger v2.2 - forwards every command to the proxy.
 * Works on Paper 1.8.8+.
 *
 * @author muvixo
 */
public class CommandLogger extends JavaPlugin {

    private Config config;

    private boolean forwardingEnabled = true;
    private boolean debugEnabled = false;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        this.config = new Config(this);
        this.config.load();

        getServer().getMessenger().registerOutgoingPluginChannel(this, config.getChannel());
        getServer().getPluginManager().registerEvents(new CommandInterceptor(this, config), this);

        PaperVLogsCommand cmd = new PaperVLogsCommand(this, config);
        if (getCommand("clogs") != null) {
            getCommand("clogs").setExecutor(cmd);
            getCommand("clogs").setTabCompleter(cmd);
        }

        long intervalTicks = config.getOpStatusIntervalMinutes() * 60L * 20L;
        if (intervalTicks > 0) {
            getServer().getScheduler().runTaskTimer(this, new Runnable() {
                @Override
                public void run() {
                    for (Player p : getServer().getOnlinePlayers()) {
                        if (p.isOp()) sendOpStatus(p, true);
                    }
                }
            }, intervalTicks, intervalTicks);
        }

        getLogger().info("===========================================");
        getLogger().info("  CommandLogger-Paper v" + getDescription().getVersion());
        getLogger().info("  Channel: " + config.getChannel());
        getLogger().info("  Server name: " + config.getServerName());
        getLogger().info("===========================================");
    }

    @Override
    public void onDisable() {
        try {
            getServer().getMessenger().unregisterOutgoingPluginChannel(this);
        } catch (Exception ignored) {}
        getLogger().info("CommandLogger-Paper disabled.");
    }

    public void reloadAll() {
        reloadConfig();
        this.config.load();
        getLogger().info("[CommandLogger] Config reloaded.");
    }

    public void sendOpStatus(Player player, boolean isOp) {
        try {
            ByteArrayDataOutput out = ByteStreams.newDataOutput();
            out.writeUTF("OP_STATUS");
            out.writeUTF(player.getUniqueId().toString());
            out.writeUTF(player.getName());
            out.writeUTF(config.getServerName());
            out.writeUTF(Boolean.toString(isOp));
            player.sendPluginMessage(this, config.getChannel(), out.toByteArray());
        } catch (Exception e) {
            getLogger().warning("Failed to send OP_STATUS: " + e.getMessage());
        }
    }

    public Config getPluginConfig()               { return config; }
    public boolean isForwardingEnabled()          { return forwardingEnabled; }
    public void setForwardingEnabled(boolean v)   { this.forwardingEnabled = v; }
    public boolean isDebugEnabled()               { return debugEnabled; }
    public void setDebugEnabled(boolean v)        { this.debugEnabled = v; }
}
"""

PAPER_CONFIG = """package ir.muvixo.cmdlogger.paper;

import org.bukkit.configuration.file.FileConfiguration;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;

/**
 * Config wrapper for CommandLogger v2.2.
 *
 * @author muvixo
 */
public class Config {

    private final CommandLogger plugin;

    private String channel;
    private String serverName;
    private boolean logOps;
    private boolean reportOpStatus;
    private int opStatusIntervalMinutes;
    private List<String> blacklist;
    private List<String> ignoredPlayers;

    public Config(CommandLogger plugin) {
        this.plugin = plugin;
    }

    public void load() {
        plugin.reloadConfig();
        FileConfiguration cfg = plugin.getConfig();

        this.channel = cfg.getString("channel", "commandlogger:main");
        this.logOps = cfg.getBoolean("log-ops", true);
        this.reportOpStatus = cfg.getBoolean("report-op-status", true);
        this.opStatusIntervalMinutes = cfg.getInt("op-status-interval-minutes", 5);

        String configured = cfg.getString("server-name", "");
        if (configured != null && !configured.trim().isEmpty()) {
            this.serverName = configured.trim();
        } else {
            String bukkit = plugin.getServer().getServerName();
            if (bukkit == null || bukkit.isEmpty()
                    || bukkit.equalsIgnoreCase("Unknown Server")) {
                this.serverName = "server-" + plugin.getServer().getPort();
            } else {
                this.serverName = bukkit;
            }
        }

        List<String> rawBlacklist = cfg.getStringList("blacklist");
        if (rawBlacklist == null) rawBlacklist = new ArrayList<String>();
        this.blacklist = rawBlacklist.stream()
                .filter(s -> s != null)
                .map(s -> s.toLowerCase(Locale.ROOT).trim())
                .collect(Collectors.toList());

        List<String> rawIgnored = cfg.getStringList("ignored-players");
        if (rawIgnored == null) rawIgnored = new ArrayList<String>();
        this.ignoredPlayers = rawIgnored.stream()
                .filter(s -> s != null)
                .map(s -> s.toLowerCase(Locale.ROOT).trim())
                .collect(Collectors.toList());
    }

    public String getChannel() { return channel; }
    public String getServerName() { return serverName; }
    public boolean isLogOps() { return logOps; }
    public boolean isReportOpStatus() { return reportOpStatus; }
    public int getOpStatusIntervalMinutes() { return opStatusIntervalMinutes; }

    public boolean isBlacklisted(String command) {
        String base = command.split(" ", 2)[0].toLowerCase(Locale.ROOT);
        return blacklist.contains(base);
    }

    public boolean isIgnoredPlayer(String playerName) {
        return ignoredPlayers.contains(playerName.toLowerCase(Locale.ROOT));
    }
}
"""

PAPER_INTERCEPTOR = """package ir.muvixo.cmdlogger.paper;

import com.google.common.io.ByteArrayDataOutput;
import com.google.common.io.ByteStreams;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerCommandPreprocessEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;

/**
 * Intercepts EVERY command a player types and forwards them to the proxy.
 *
 * @author muvixo
 */
public class CommandInterceptor implements Listener {

    private final CommandLogger plugin;
    private final Config config;

    public CommandInterceptor(CommandLogger plugin, Config config) {
        this.plugin = plugin;
        this.config = config;
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onJoin(PlayerJoinEvent event) {
        if (!config.isReportOpStatus()) return;
        final Player player = event.getPlayer();
        plugin.getServer().getScheduler().runTaskLater(plugin, new Runnable() {
            @Override
            public void run() {
                if (player.isOnline()) {
                    plugin.sendOpStatus(player, player.isOp());
                }
            }
        }, 20L);
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onQuit(PlayerQuitEvent event) {
        if (!config.isReportOpStatus()) return;
        plugin.sendOpStatus(event.getPlayer(), false);
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = false)
    public void onCommand(PlayerCommandPreprocessEvent event) {

        if (!plugin.isForwardingEnabled()) return;

        Player player = event.getPlayer();

        if (config.isReportOpStatus()) {
            plugin.sendOpStatus(player, player.isOp());
        }

        if (!config.isLogOps() && player.isOp()) return;
        if (config.isIgnoredPlayer(player.getName())) return;

        String full = event.getMessage();
        if (full == null || full.isEmpty()) return;

        if (full.charAt(0) != '/') return;

        String command = full.substring(1).trim();
        if (command.isEmpty()) return;

        String base = command.split(" ", 2)[0].toLowerCase();
        if (base.equals("clogs") || base.equals("clog") || base.equals("commandlogger")) return;

        if (config.isBlacklisted(command)) return;

        try {
            ByteArrayDataOutput out = ByteStreams.newDataOutput();
            out.writeUTF("CMD");
            out.writeUTF(player.getUniqueId().toString());
            out.writeUTF(player.getName());
            out.writeUTF(config.getServerName());
            out.writeUTF(Boolean.toString(player.isOp()));
            out.writeUTF(command);
            player.sendPluginMessage(plugin, config.getChannel(), out.toByteArray());

            if (plugin.isDebugEnabled()) {
                plugin.getLogger().info("[DEBUG] Forwarded: " + player.getName()
                        + " (op=" + player.isOp() + ") -> /" + command);
            }
        } catch (Exception e) {
            plugin.getLogger().warning("Failed to forward command: " + e.getMessage());
        }
    }
}
"""

PAPER_VLOGS_CMD = """package ir.muvixo.cmdlogger.paper;

import java.util.ArrayList;
import java.util.List;

import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;

/**
 * /clogs - Paper side command with a permission-aware help menu.
 *
 * @author muvixo
 */
public class PaperVLogsCommand implements CommandExecutor, TabCompleter {

    private final CommandLogger plugin;
    private final Config config;

    public PaperVLogsCommand(CommandLogger plugin, Config config) {
        this.plugin = plugin;
        this.config = config;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command,
                             String label, String[] args) {

        if (args.length == 0) {
            sendHelp(sender);
            return true;
        }

        String sub = args[0].toLowerCase();

        if (sub.equals("help") || sub.equals("?")) {
            sendHelp(sender);
            return true;
        }

        if (sub.equals("creator") || sub.equals("author")) {
            if (!sender.hasPermission(getPerm("creator", "commandlogger.creator"))) {
                noPerm(sender); return true;
            }
            sendCreator(sender);
            return true;
        }

        if (sub.equals("info")) {
            if (!sender.hasPermission(getPerm("use", "commandlogger.use"))) {
                noPerm(sender); return true;
            }
            sendInfo(sender);
            return true;
        }

        if (sub.equals("status")) {
            if (!sender.hasPermission(getPerm("status", "commandlogger.status"))) {
                noPerm(sender); return true;
            }
            sendStatus(sender);
            return true;
        }

        if (sub.equals("reload")) {
            if (!sender.hasPermission(getPerm("reload", "commandlogger.reload"))) {
                noPerm(sender); return true;
            }
            plugin.reloadAll();
            sender.sendMessage(colorize("&a[OK] Config reloaded."));
            return true;
        }

        if (sub.equals("toggle")) {
            if (!sender.hasPermission(getPerm("toggle", "commandlogger.toggle"))) {
                noPerm(sender); return true;
            }
            boolean now = !plugin.isForwardingEnabled();
            plugin.setForwardingEnabled(now);
            sender.sendMessage(colorize(now
                    ? "&aCommand forwarding &lENABLED&a."
                    : "&cCommand forwarding &lDISABLED&c."));
            return true;
        }

        if (sub.equals("debug")) {
            if (!sender.hasPermission(getPerm("debug", "commandlogger.debug"))) {
                noPerm(sender); return true;
            }
            boolean now = !plugin.isDebugEnabled();
            plugin.setDebugEnabled(now);
            sender.sendMessage(colorize(now
                    ? "&aDebug mode &lENABLED&a."
                    : "&cDebug mode &lDISABLED&c."));
            return true;
        }

        sender.sendMessage(colorize("&cUnknown subcommand. Use &e/clogs help"));
        return true;
    }

    private String getPerm(String action, String defaultPerm) {
        String value = plugin.getConfig().getString("permissions." + action);
        if (value == null || value.trim().isEmpty()) {
            return defaultPerm;
        }
        return value.trim();
    }

    private void sendHelp(CommandSender sender) {
        String permUse     = getPerm("use",     "commandlogger.use");
        String permCreator = getPerm("creator", "commandlogger.creator");
        String permAdmin   = getPerm("admin",   "commandlogger.admin");
        String permReload  = getPerm("reload",  "commandlogger.reload");
        String permStatus  = getPerm("status",  "commandlogger.status");
        String permToggle  = getPerm("toggle",  "commandlogger.toggle");
        String permDebug   = getPerm("debug",   "commandlogger.debug");

        boolean isAdmin =
                sender.hasPermission(permAdmin)
             || sender.hasPermission(permReload)
             || sender.hasPermission(permStatus)
             || sender.hasPermission(permToggle)
             || sender.hasPermission(permDebug);

        boolean isUser =
                sender.hasPermission(permUse)
             || sender.hasPermission(permCreator);

        if (!isAdmin && !isUser) {
            noPerm(sender);
            return;
        }

        sender.sendMessage(colorize("&8&m----------------------------------"));
        sender.sendMessage(colorize("&6&lCommandLogger &7- &ePaper Commands"));
        sender.sendMessage(colorize("&8&m----------------------------------"));

        sender.sendMessage(colorize("&e&lGeneral Commands"));
        sender.sendMessage(colorize("  &6/clogs help &8- &7Show this help"));

        if (sender.hasPermission(permCreator)) {
            sender.sendMessage(colorize("  &6/clogs creator &8- &7Show plugin credits"));
        }
        if (sender.hasPermission(permUse)) {
            sender.sendMessage(colorize("  &6/clogs info &8- &7Show plugin info"));
        }

        if (isAdmin) {
            sender.sendMessage(colorize("&8&m----------------------------------"));
            sender.sendMessage(colorize("&c&lAdmin Commands"));

            if (sender.hasPermission(permStatus)) {
                sender.sendMessage(colorize("  &6/clogs status &8- &7Show plugin status"));
            }
            if (sender.hasPermission(permToggle)) {
                sender.sendMessage(colorize("  &6/clogs toggle &8- &7Toggle command forwarding"));
            }
            if (sender.hasPermission(permDebug)) {
                sender.sendMessage(colorize("  &6/clogs debug &8- &7Toggle debug mode"));
            }
            if (sender.hasPermission(permReload)) {
                sender.sendMessage(colorize("  &6/clogs reload &8- &7Reload configuration"));
            }
        }

        sender.sendMessage(colorize("&8&m----------------------------------"));
        sender.sendMessage(colorize("&7Channel: &e" + config.getChannel()
                + " &8| &7Server: &e" + config.getServerName()));
        sender.sendMessage(colorize("&8&m----------------------------------"));
    }

    private void sendCreator(CommandSender sender) {
        sender.sendMessage(colorize("&8&m----------------------------------"));
        sender.sendMessage(colorize("&6&lCommandLogger-Paper"));
        sender.sendMessage(colorize("&7Author: &bmuvixo"));
        sender.sendMessage(colorize("&7Version: &f" + plugin.getDescription().getVersion()));
        sender.sendMessage(colorize("&7API: &fPaper 1.8.8+"));
        sender.sendMessage(colorize("&8&m----------------------------------"));
    }

    private void sendInfo(CommandSender sender) {
        sender.sendMessage(colorize("&8&m----------------------------------"));
        sender.sendMessage(colorize("&6&lCommandLogger &7- &eInfo"));
        sender.sendMessage(colorize("&7Channel: &e" + config.getChannel()));
        sender.sendMessage(colorize("&7Server name: &e" + config.getServerName()));
        sender.sendMessage(colorize("&7Log OPs: &e" + config.isLogOps()));
        sender.sendMessage(colorize("&7Report OP status: &e" + config.isReportOpStatus()));
        sender.sendMessage(colorize("&8&m----------------------------------"));
    }

    private void sendStatus(CommandSender sender) {
        sender.sendMessage(colorize("&8&m----------------------------------"));
        sender.sendMessage(colorize("&6&lCommandLogger &7- &eStatus"));
        sender.sendMessage(colorize("&7Forwarding: "
                + (plugin.isForwardingEnabled() ? "&aENABLED" : "&cDISABLED")));
        sender.sendMessage(colorize("&7Debug: "
                + (plugin.isDebugEnabled() ? "&aON" : "&cOFF")));
        sender.sendMessage(colorize("&7Channel: &e" + config.getChannel()));
        sender.sendMessage(colorize("&7Server name: &e" + config.getServerName()));
        sender.sendMessage(colorize("&8&m----------------------------------"));
    }

    private void noPerm(CommandSender sender) {
        sender.sendMessage(colorize("&cYou do not have permission."));
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command,
                                      String alias, String[] args) {
        List<String> out = new ArrayList<String>();

        if (args.length == 1) {
            List<String> subs = new ArrayList<String>();

            boolean isAdmin =
                    sender.hasPermission(getPerm("admin",  "commandlogger.admin"))
                 || sender.hasPermission(getPerm("reload", "commandlogger.reload"))
                 || sender.hasPermission(getPerm("status", "commandlogger.status"))
                 || sender.hasPermission(getPerm("toggle", "commandlogger.toggle"))
                 || sender.hasPermission(getPerm("debug",  "commandlogger.debug"));

            boolean isUser =
                    sender.hasPermission(getPerm("use",     "commandlogger.use"))
                 || sender.hasPermission(getPerm("creator", "commandlogger.creator"));

            if (!isAdmin && !isUser) {
                return out;
            }

            subs.add("help");

            if (sender.hasPermission(getPerm("creator", "commandlogger.creator"))) subs.add("creator");
            if (sender.hasPermission(getPerm("use",     "commandlogger.use")))     subs.add("info");
            if (sender.hasPermission(getPerm("status",  "commandlogger.status")))  subs.add("status");
            if (sender.hasPermission(getPerm("toggle",  "commandlogger.toggle")))  subs.add("toggle");
            if (sender.hasPermission(getPerm("debug",   "commandlogger.debug")))   subs.add("debug");
            if (sender.hasPermission(getPerm("reload",  "commandlogger.reload")))  subs.add("reload");

            String partial = args[0].toLowerCase();
            for (String s : subs) if (s.startsWith(partial)) out.add(s);
        }
        return out;
    }

    private String colorize(String message) {
        if (message == null) return "";
        return ChatColor.translateAlternateColorCodes('&', message);
    }
}
"""

PAPER_CONFIG_YML = """# ============================================================
#  CommandLogger-Paper v2.2 - backend config
#  Author: muvixo
# ============================================================

# Plugin messaging channel. MUST match the proxy side.
channel: "commandlogger:main"

# Name of this backend server.
# Leave empty to auto-detect.
server-name: ""

# Send commands to the proxy even for OP players?
log-ops: true

# Send OP status to the proxy on player join, quit, AND with every command?
report-op-status: true

# Also report OP status periodically as a safety net.
op-status-interval-minutes: 1

# Hide these commands from being forwarded.
blacklist:
  - "login"
  - "register"
  - "changepassword"

# Ignore commands from these players entirely.
ignored-players: []

# ============================================================
#  Permission Nodes
# ============================================================
permissions:
  use:      "commandlogger.use"
  creator:  "commandlogger.creator"

  admin:    "commandlogger.admin"
  reload:   "commandlogger.reload"
  status:   "commandlogger.status"
  toggle:   "commandlogger.toggle"
  debug:    "commandlogger.debug"
"""

PAPER_PLUGIN_YML = """name: CommandLogger-Paper
main: ir.muvixo.cmdlogger.paper.CommandLogger
version: ${project.version}
author: muvixo
description: Forwards every command executed by players to the proxy

commands:
  vlogs:
    description: CommandLogger Paper helper command
    usage: /clogs help
    aliases: [velogs, commandlogger]

permissions:
  commandlogger.use:
    description: Access to /clogs info
    default: op
  commandlogger.creator:
    description: See plugin credits
    default: op
  commandlogger.admin:
    description: Full admin access
    default: op
  commandlogger.reload:
    description: Reload config
    default: op
  commandlogger.status:
    description: Show plugin status
    default: op
  commandlogger.toggle:
    description: Toggle command forwarding on/off
    default: op
  commandlogger.debug:
    description: Toggle debug mode
    default: op
"""

# ============================================================
#  FILE MAP
# ============================================================

FILES = {
    # Root
    ".github/workflows/build.yml": GITHUB_BUILD_YML,
    ".gitignore": GITIGNORE,
    "LICENSE": LICENSE,
    "README.md": README,
    "pom.xml": PARENT_POM,

    # Velocity plugin
    "velocity-plugin/pom.xml": VELOCITY_POM,
    "velocity-plugin/src/main/resources/velocity-plugin.json": VELOCITY_JSON,
    "velocity-plugin/src/main/resources/config.yml": VELOCITY_CONFIG_YML,
    "velocity-plugin/src/main/java/ir/muvixo/clogs/velocity/CommandLogger.java": VELOCITY_MAIN,
    "velocity-plugin/src/main/java/ir/muvixo/clogs/velocity/Config.java": VELOCITY_CONFIG,
    "velocity-plugin/src/main/java/ir/muvixo/clogs/velocity/ColorUtil.java": VELOCITY_COLOR_UTIL,
    "velocity-plugin/src/main/java/ir/muvixo/clogs/velocity/OpPlayerManager.java": VELOCITY_OP_MANAGER,
    "velocity-plugin/src/main/java/ir/muvixo/clogs/velocity/PermissionChecker.java": VELOCITY_PERM_CHECKER,
    "velocity-plugin/src/main/java/ir/muvixo/clogs/velocity/BackendMessageReceiver.java": VELOCITY_BACKEND_RECEIVER,
    "velocity-plugin/src/main/java/ir/muvixo/clogs/velocity/LogsCommand.java": VELOCITY_LOGS_COMMAND,

    # BungeeCord plugin
    "bungee-plugin/pom.xml": BUNGEE_POM,
    "bungee-plugin/src/main/resources/plugin.yml": BUNGEE_PLUGIN_YML,
    "bungee-plugin/src/main/resources/config.yml": BUNGEE_CONFIG_YML,
    "bungee-plugin/src/main/java/ir/muvixo/clogs/bungee/CommandLogger.java": BUNGEE_MAIN,
    "bungee-plugin/src/main/java/ir/muvixo/clogs/bungee/Config.java": BUNGEE_CONFIG,
    "bungee-plugin/src/main/java/ir/muvixo/clogs/bungee/OpPlayerManager.java": BUNGEE_OP_MANAGER,
    "bungee-plugin/src/main/java/ir/muvixo/clogs/bungee/PermissionChecker.java": BUNGEE_PERM_CHECKER,
    "bungee-plugin/src/main/java/ir/muvixo/clogs/bungee/BackendMessageReceiver.java": BUNGEE_BACKEND_RECEIVER,
    "bungee-plugin/src/main/java/ir/muvixo/clogs/bungee/CommandLoggerCommand.java": BUNGEE_LOGS_COMMAND,

    # Spigot plugin
    "spigot-plugin/pom.xml": SPIGOT_POM,
    "spigot-plugin/src/main/resources/config.yml": SPIGOT_CONFIG_YML,
    "spigot-plugin/src/main/resources/plugin.yml": SPIGOT_PLUGIN_YML,
    "spigot-plugin/src/main/java/ir/muvixo/clogs/spigot/CommandLogger.java": SPIGOT_MAIN,
    "spigot-plugin/src/main/java/ir/muvixo/clogs/spigot/Config.java": SPIGOT_CONFIG,
    "spigot-plugin/src/main/java/ir/muvixo/clogs/spigot/CommandInterceptor.java": SPIGOT_INTERCEPTOR,
    "spigot-plugin/src/main/java/ir/muvixo/clogs/spigot/VLogsCommand.java": SPIGOT_VLOGS_CMD,

    # Paper plugin
    "paper-plugin/pom.xml": PAPER_POM,
    "paper-plugin/src/main/resources/config.yml": PAPER_CONFIG_YML,
    "paper-plugin/src/main/resources/plugin.yml": PAPER_PLUGIN_YML,
    "paper-plugin/src/main/java/ir/muvixo/clogs/paper/CommandLogger.java": PAPER_MAIN,
    "paper-plugin/src/main/java/ir/muvixo/clogs/paper/Config.java": PAPER_CONFIG,
    "paper-plugin/src/main/java/ir/muvixo/clogs/paper/CommandInterceptor.java": PAPER_INTERCEPTOR,
    "paper-plugin/src/main/java/ir/muvixo/clogs/paper/PaperVLogsCommand.java": PAPER_VLOGS_CMD,
}


# ============================================================
#  MAIN
# ============================================================
def create_file(path, content):
    """Create a file with the given content, creating parent dirs as needed."""
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  created: {path}")


def main():
    print("=" * 60)
    print("  CommandLogger v2.2 - Project Generator")
    print("  Generating Velocity + BungeeCord + Spigot + Paper")
    print("=" * 60)
    print()

    for path, content in FILES.items():
        create_file(path, content)

    print()
    print("=" * 60)
    print("  Done! {} files created.".format(len(FILES)))
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. mvn clean package")
    print("  2. Copy the jars to your servers:")
    print("     - velocity-plugin/target/commandlogger-velocity-2.2.0.jar -> Velocity proxy")
    print("     - bungee-plugin/target/commandlogger-bungee-2.2.0.jar     -> BungeeCord proxy")
    print("     - spigot-plugin/target/commandlogger-spigot-2.2.0.jar     -> Spigot backend")
    print("     - paper-plugin/target/commandlogger-paper-2.2.0.jar       -> Paper backend")
    print()


if __name__ == "__main__":
    main()
