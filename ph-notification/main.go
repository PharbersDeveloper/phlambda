package main

import (
	"context"
	"encoding/json"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-lambda-go/lambdacontext"
	"log"
)

type PhEventResponse struct {
	Responses []SQSResponse `json:"Responses"`
}

//Handler is function executed by lambda engine
func handleRequest(ctx context.Context, event events.SQSEvent) (PhEventResponse, error) {

	// event
	eventJson, _ := json.MarshalIndent(event, "", "  ")
	log.Printf("EVENT: %s", eventJson)
	// request context
	lc, _ := lambdacontext.FromContext(ctx)
	log.Printf("REQUEST ID: %s", lc.AwsRequestID)
	// global variable
	log.Printf("FUNCTION NAME: %s", lambdacontext.FunctionName)
	// context method
	deadline, _ := ctx.Deadline()
	log.Printf("DEADLINE: %s", deadline)

	res := PhEventResponse{
		Responses: make([]SQSResponse, 0),
	}

	for _, sqsMsg := range event.Records {
		res.Responses = append(res.Responses, DealSQSMessage(ctx, sqsMsg))
	}

	return res, nil
}

func main() {
	lambda.Start(handleRequest)
}
