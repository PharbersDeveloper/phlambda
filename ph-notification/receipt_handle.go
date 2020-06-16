package main

import (
	"context"
	"github.com/aws/aws-lambda-go/events"
	"log"
	"os"
	"plugin"
)

type SQSResponse struct {
	MessageId     string            `json:"messageId"`
	ReceiptHandle string            `json:"receiptHandle"`
	Status        string            `json:"status"`
	ErrMsg        string            `json:"errMsg"`
	Attributes    map[string]string `json:"attributes"`
}

func DealSQSMessage(ctx context.Context, sqsMsg events.SQSMessage) SQSResponse {

	select {
	case <-ctx.Done():
		log.Println("Context is done.")
		os.Exit(1)
	default:
		return handleSQSMsg(sqsMsg)
	}

	return SQSResponse{}
}

func handleSQSMsg(sqsMsg events.SQSMessage) SQSResponse {
	res := SQSResponse{
		MessageId: sqsMsg.MessageId,
		ReceiptHandle: sqsMsg.ReceiptHandle,
		Status: "ok",
		ErrMsg: "",
		Attributes: nil,
	}

	layerDir := "/opt/"
	// Load plugin
	pluginModule, err := plugin.Open(layerDir + sqsMsg.ReceiptHandle + ".so")
	if err != nil {
		log.Printf("Unable to load %s module", sqsMsg.ReceiptHandle)
		return dealErrorResponse(res, err)
	}
	//Load symbol
	handleSQSMsgSymbol, err := pluginModule.Lookup(sqsMsg.ReceiptHandle)
	if err != nil {
		log.Printf("Unable to load %s symbol", sqsMsg.ReceiptHandle)
		return dealErrorResponse(res, err)
	}

	//Cast symbol to func
	handleSQSMsgFunc := handleSQSMsgSymbol.(func(events.SQSMessage) error)

	err = handleSQSMsgFunc(sqsMsg)
	if err != nil {
		return dealErrorResponse(res, err)
	}

	return res
}

func dealErrorResponse(res SQSResponse, err error) SQSResponse {
	res.ErrMsg = err.Error()
	res.Status = "error"
	return res
}
