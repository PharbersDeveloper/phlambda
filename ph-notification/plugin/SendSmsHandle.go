package main

import (
	"github.com/aliyun/alibaba-cloud-sdk-go/sdk"
	"github.com/aliyun/alibaba-cloud-sdk-go/sdk/requests"
	"github.com/aws/aws-lambda-go/events"
	"log"
	"os"
)

func SendSmsHandle(sqsMsg events.SQSMessage) error {

	regionId := os.Getenv("PH_SMS__REGION_ID")
	accessKeyId := os.Getenv("PH_SMS__ACCESS_KEY_ID")
	accessKeySecret := os.Getenv("PH_SMS__ACCESS_KEY_SECRET")
	domain := os.Getenv("PH_SMS__DOMAIN")
	version := os.Getenv("PH_SMS__VERSION")
	signName := os.Getenv("PH_SMS__SIGN_NAME")
	templateCode := os.Getenv("PH_SMS__TEMPLATE_CODE")

	client, err := sdk.NewClientWithAccessKey(regionId, accessKeyId, accessKeySecret)
	if err != nil {
		panic(err.Error())
	}

	req := requests.NewCommonRequest()
	req.Method = "POST"
	req.Scheme = "https"
	req.Domain = domain
	req.Version = version
	req.ApiName = "SendSms"
	req.QueryParams["RegionId"] = regionId
	req.QueryParams["PhoneNumbers"] = sqsMsg.Attributes["PhoneNumbers"]
	req.QueryParams["SignName"] = signName
	req.QueryParams["TemplateCode"] = templateCode
	req.QueryParams["TemplateParam"] = "{\"code\":\"" + sqsMsg.Attributes["Code"] + "\"}"
	res, err := client.ProcessCommonRequest(req)
	log.Printf("SendSmsHandle response=(%v)", res)
	return err
}
