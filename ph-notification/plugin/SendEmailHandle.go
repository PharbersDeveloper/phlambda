package main

import (
	"encoding/json"
	"errors"
	"github.com/aws/aws-lambda-go/events"
	"github.com/go-gomail/gomail"
)

type EmailInfo struct {
	ServerHost  string `json:"server-host"`
	ServerPort  int    `json:"server-port"`
	From        string `json:"from"`
	Pwd         string `json:"pwd"`
	To          string `json:"to"`
	Subject     string `json:"subject"`
	ContentType string `json:"content-type"`
	Content     string `json:"content"`
}

func SendEmailHandle(sqsMsg events.SQSMessage) error {

	if sqsMsg.ReceiptHandle != "SendEmailHandle" {
		return errors.New("Not SendEmailHandle SQS Msg. ")
	}

	var emailInfo EmailInfo
	err := json.Unmarshal([]byte(sqsMsg.Body), &emailInfo)
	if err != nil {
		return err
	}

	m := gomail.NewMessage()
	m.SetHeader("From", emailInfo.From)
	m.SetHeader("To", emailInfo.To)
	m.SetHeader("Subject", emailInfo.Subject)
	m.SetBody(emailInfo.ContentType, emailInfo.Content)

	d := gomail.NewDialer(emailInfo.ServerHost, emailInfo.ServerPort, emailInfo.From, emailInfo.Pwd)
	err = d.DialAndSend(m)
	return err
}
