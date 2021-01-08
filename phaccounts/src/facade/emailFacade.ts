import axios from "axios"

class EmailFacade {

    public async sendEmail(to: string, subject: string, contentType: string, content: string) {
        const parameter = {to, subject: subject ||  process.env.SUBJECT, contentType, content}
        return axios({
            auth: {
                username: "demo",
                password: "demo"
            },
            method: "POST",
            url: process.env.AIRFLOWURL,
            data: JSON.stringify({conf: parameter}),
            headers: {"Content-Type": "application/json;charset=utf-8", "Accept": "application/json;charset=utf-8"}
        })
    }
}
export default EmailFacade
