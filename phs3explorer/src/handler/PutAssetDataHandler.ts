import { IStore, Logger, Register, StoreEnum } from "phnodelayer"

export default class PutAssetDataHandler {

    async PutAssetData(event: any) {
        const store = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
        await store.open()
        const { owner, tempfile, asset: { fileName, extension, size, labels, description, type } } = event
        const record = {
            name: fileName,
            extension,
            owner,
            isNewVersion: true,
            size,
            labels,
            description,
            type,
            source: `user/${owner}/${tempfile}`
        }
        await store.create("asset", record)
        await store.close()
    }
}
