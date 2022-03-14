import express from "express";
import http from "http";
import { WebSocketServer } from "ws";
import mongoose from "mongoose";

import RobotSocket from "./websocket/robotSocket";
import Logger from "./utils/logger";
import { DB_URL, PORT, CLIENT_TYPE, COMMAND_TYPE } from "./definition/index";
import DBHelper from "./db/dbHelper";

const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

mongoose.connect(DB_URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

const db = mongoose.connection;
const logger = new Logger();
const dbHelper = new DBHelper();

db.on("error", (error) => {
    logger.error(error);
});

db.once("open", () => {
    wss.on("connection", (ws) => {
        ws.onmessage = (mes) => {
            const parsedData = JSON.parse(mes.data);
            const { command, payload } = parsedData;
            logger.message(`Command: ${command}`);
            logger.message("Payload: ", payload);
            if (command === COMMAND_TYPE.BOARDINFO) {
                const type = payload.type;
                switch (type) {
                    case CLIENT_TYPE.ROBOT: {
                        const { robotName, ip } = payload;
                        const robotSocket = new RobotSocket(ws, robotName, ip, dbHelper, logger);
                        robotSocket.handleMessage();
                        break;
                    }
                    case CLIENT_TYPE.WEB: {
                        break;
                    }
                    default: {
                        // error
                        logger.error(`Invalid type ${type} for connection`);
                        break;
                    }
                }
            }
        };
    });

    server.listen(PORT, () => {
        logger.message(`Server listening on port ${PORT}`);
    });
});
