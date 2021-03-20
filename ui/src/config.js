// This file exposes .env & .env-cmd configuration properties to the rest of the application.
// No other code should import or use the process.env variables aside from importing this file.
const name = process.env.REACT_APP_NAME;
const version = process.env.REACT_APP_VERSION;
const environment = process.env.REACT_APP_ENVIRONMENT;
const backendPath = process.env.REACT_APP_BACKEND_URL;

export { environment, version, name, backendPath };
