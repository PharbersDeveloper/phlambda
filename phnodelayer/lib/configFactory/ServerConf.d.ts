import { MongoConf } from './MongoConf';
import { MysqlConf } from './MysqlConf';
import { PostgresConf } from './PostgresConf';
import { RedisConf } from './RedisConf';
export declare class ServerConf {
    project: string;
    postgres: PostgresConf;
    mongo: MongoConf;
    mysql: MysqlConf;
    redis: RedisConf;
}
