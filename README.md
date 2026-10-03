# VelocityLogs v2.2

Logs **every command** any player types on any backend server and broadcasts
them to staff / OP players on the proxy.

Supports **Velocity**, **BungeeCord 1.8+**, **Spigot 1.8+**, and **Paper 1.8+**.

**Author:** muvixo

## What's new in v2.2

- **BungeeCord 1.8 support** - full plugin messaging + OP tracking.
- **Paper support** - native Paper 1.8+ backend plugin.
- **Bulletproof OP detection** - OP status is attached to *every* command.
- **UUID-based tracking** - no more name-change or case bugs.
- **`/logs op <player>` / `/logs unop <player>`** - manual overrides.
- **`/logs list`** - see all currently tracked OPs.
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
| `/logs` | Show plugin info |
| `/logs help` | Show help |
| `/logs reload` | Reload config |
| `/logs debug <player>` | Diagnose a player's permissions |
| `/logs status <player>` | Same as debug |
| `/logs op <player>` | Manually mark player as OP |
| `/logs unop <player>` | Manually unmark player |
| `/logs list` | List all tracked OPs |

## Build

```bash
mvn clean package
```

Outputs:
- `velocity-plugin/target/velocity-logs-velocity-2.2.0.jar`
- `bungee-plugin/target/velocity-logs-bungee-2.2.0.jar`
- `spigot-plugin/target/velocity-logs-spigot-2.2.0.jar`
- `paper-plugin/target/velocity-logs-paper-2.2.0.jar`

## Setup

### 1. Install the proxy plugin
- **Velocity:** drop `velocity-logs-velocity-2.2.0.jar` into `plugins/`
- **BungeeCord:** drop `velocity-logs-bungee-2.2.0.jar` into `plugins/`

### 2. Install the backend plugin
- **Spigot:** drop `velocity-logs-spigot-2.2.0.jar` into `plugins/`
- **Paper:** drop `velocity-logs-paper-2.2.0.jar` into `plugins/`

### 3. Configure
Make sure `channel` matches on both proxy and backend configs.
Default: `velocitylogs:main`

### 4. Register the channel (BungeeCord)
In your BungeeCord `config.yml`, ensure `bungeecord: true` is set on the
Spigot/Paper backend servers so plugin messaging works.
