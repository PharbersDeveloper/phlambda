package main

import (
	"encoding/json"
	"github.com/aws/aws-lambda-go/events"
	"io/ioutil"
	"testing"
)

func TestSendEmail(t *testing.T) {
	type args struct {
		sqsMsg events.SQSMessage
	}

	inputJson := ReadJSONFromFile(t, "test/send_email-message.json")
	var sqsMes events.SQSMessage
	err := json.Unmarshal(inputJson, &sqsMes)
	if err != nil {
		t.Errorf("could not unmarshal event. details: %v", err)
	}

	tests := []struct {
		name    string
		args    args
		wantErr bool
	}{
		// TODO: Add test cases.
		{
			name:"test1",
			args:args{sqsMsg:sqsMes},
			wantErr:false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if err := SendEmailHandle(tt.args.sqsMsg); (err != nil) != tt.wantErr {
				t.Errorf("SendEmail() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

func ReadJSONFromFile(t *testing.T, inputFile string) []byte {
	inputJSON, err := ioutil.ReadFile(inputFile)
	if err != nil {
		t.Errorf("could not open test file. details: %v", err)
	}

	return inputJSON
}