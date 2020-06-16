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
	MessageHandle string            `json:"messageHandle"`
	Status        string            `json:"status"`
	ErrMsg        string            `json:"errMsg"`
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
		MessageId:     sqsMsg.MessageId,
		MessageHandle: sqsMsg.Body,
		Status:        "ok",
		ErrMsg:        "",
	}

	layerDir := "/opt/"
	// Load plugin
	pluginModule, err := plugin.Open(layerDir + sqsMsg.Body + ".so")
	if err != nil {
		log.Printf("Unable to load %s module", sqsMsg.Body)
		return dealErrorResponse(res, err)
	}
	//Load symbol
	handleSQSMsgSymbol, err := pluginModule.Lookup(sqsMsg.Body)
	if err != nil {
		log.Printf("Unable to load %s symbol", sqsMsg.Body)
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
