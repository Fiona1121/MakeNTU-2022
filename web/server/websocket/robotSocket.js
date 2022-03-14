import { COMMAND_TYPE } from "../definition/index";

class RobotSocket {
    constructor(ws, robotName, ip, dbHelper, logger) {
        this.ws = null;
        this.robotName = robotName;
        this.ip = ip;
        this.dbHelper = dbHelper;
        this.logger = logger;
        this.methods = {
            [COMMAND_TYPE.SAVEDATA]: this.saveData,
        };
        this.init(ws);
    }
    init = (ws) => {
        this.ws = ws;
        this.logger.connect(`Robot ${this.robotName} connected, ip: ${this.ip}`);
        this.handleDisconnect();
    };
    handleMessage = () => {
        this.ws.onmessage = (mes) => {
            const parsedData = JSON.parse(mes.data);
            const { command, payload } = parsedData;
            this.logger.message(`${this.robotName} send request: ${command}`);
            this.logger.message("Payload: ", payload);
            this.methods[command](payload);
        };
    };
    handleDisconnect = () => {
        this.ws.onclose = (mes) => {
            this.logger.disconnect(`Robot ${this.robotName} disconnected`);
        };
    };
    saveData = (data) => {};
}

export default RobotSocket;
