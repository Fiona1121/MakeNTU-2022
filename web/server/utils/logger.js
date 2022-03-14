class Logger {
    error = (mes) => {
        console.error("[Error] ", mes);
    };
    connect = (mes) => {
        console.log("[Connect] ", mes);
    };
    disconnect = (mes) => {
        console.log("[Disconnect] ", mes);
    };
    message = (mes) => {
        console.log("[Message] ", mes);
    };
}

export default Logger;
