const HOST = import.meta.env.PROD ? "" : "http://0.0.0.0:8000";

const configureEndpoint = (endpoint: string) => `${HOST}/${endpoint}`;

export default configureEndpoint;
