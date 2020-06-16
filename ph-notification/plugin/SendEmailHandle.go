package main

import (
	"errors"
	"github.com/aws/aws-lambda-go/events"
	"github.com/go-gomail/gomail"
	"os"
	"strconv"
)

func SendEmailHandle(sqsMsg events.SQSMessage) error {

	if sqsMsg.ReceiptHandle != "SendEmailHandle" {
		return errors.New("Not SendEmailHandle SQS Msg. ")
	}

	host := os.Getenv("PH_EMAIL__SERVER_HOST")
	portStr := os.Getenv("PH_EMAIL__SERVER_PORT")
	port, err := strconv.Atoi(portStr)
	if err != nil {
		return err
	}
	user := os.Getenv("PH_EMAIL__USER")
	pswd := os.Getenv("PH_EMAIL__PSWD")

	d := gomail.NewDialer(host, port, user, pswd)

	m := gomail.NewMessage()
	m.SetHeader("From", user)
	m.SetHeader("To", sqsMsg.Attributes["To"])
	m.SetHeader("Subject", sqsMsg.Attributes["Subject"])
	m.SetBody(sqsMsg.Attributes["ContentType"], sqsMsg.Attributes["Content"])

	err = d.DialAndSend(m)
	return err
}
