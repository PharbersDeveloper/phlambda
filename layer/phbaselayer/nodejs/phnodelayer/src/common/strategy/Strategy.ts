import IStrategy from "./IStrategy"
import DBModel from "../models/DBModel"

// tslint:disable-next-line:no-namespace
export namespace Strategy {
    export class PostgresStrategy implements IStrategy {
        choose(config: DBModel): any {
            return {
                connection: {
                    name: config.name,
                    database: config.database,
                    user: config.user,
                    password: config.password,
                    host: config.host,
                    port: config.port,
                    ssl: config.ssl,
                    max: config.max,
                    idleTimeoutMillis: config.idleTimeoutMillis,
                    connectionTimeoutMillis: config.connectionTimeoutMillis,
                }
            }
        }
    }

    // tslint:disable-next-line:max-classes-per-file
    export class RedisStrategy implements IStrategy {
        choose(config: DBModel): any {
            return {
                name: config.name,
                host: config.host,
                port: config.port,
                options: {
                    db: config.database,
                    username: config.user,
                    password: config.password,
                    commandTimeout: config.idleTimeoutMillis,
                    connectTimeout: config.connectionTimeoutMillis,
                }
            }
        }
    }

    // tslint:disable-next-line:max-classes-per-file
    export class MongoStrategy implements IStrategy {
        choose(config: DBModel): any {
            return {
                connection: {
                    name: config.name,
                    database: config.database,
                    user: config.user,
                    password: config.password,
                    host: config.host,
                    port: config.port,
                    ssl: config.ssl,
                    max: config.max,
                    idleTimeoutMillis: config.idleTimeoutMillis,
                    connectionTimeoutMillis: config.connectionTimeoutMillis,
                }
            }
        }
    }

}
