package ir.muvixo.cmdlogger.velocity;

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
 * Created by Muvixo
 */
public class BackendMessageReceiver {

    private static final DateTimeFormatter TIME_FORMAT = DateTimeFormatter.ofPattern("HH:mm:ss");

    private final ProxyServer server;
    private final Logger logger;
    private final Config config;
    private final Messages messages;
    private final OpPlayerManager opManager;
    private final PermissionChecker permChecker;
    private final MinecraftChannelIdentifier channel;

    public BackendMessageReceiver(ProxyServer server, Logger logger, Config config, Messages messages,
                                  OpPlayerManager opManager, PermissionChecker permChecker) {
        this.server = server;
        this.logger = logger;
        this.config = config;
        this.messages = messages;
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
            logger.info(messages.raw(isOp ? "console-op-marked" : "console-op-unmarked",
                    "player", name, "server", serverName));
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
        Component message = messages.get("log-format",
                "player", playerName,
                "server", serverName,
                "command", command,
                "time", time);

        int total = 0, sent = 0;
        for (Player online : server.getAllPlayers()) {
            total++;
            if (!permChecker.canSee(online)) continue;
            if (!config.isShowToSelf()
                    && online.getUsername().equalsIgnoreCase(playerName)) continue;
            online.sendMessage(message);
            sent++;
        }

        if (config.isLogToConsole()) {
            logger.info(messages.raw("console-command-log",
                    "player", playerName,
                    "server", serverName,
                    "command", command,
                    "online", total,
                    "sent", sent,
                    "ops", opManager.getOpCount()));
        }
    }
}
