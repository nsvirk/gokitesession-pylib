package main

/*
#include <stdlib.h>
*/
import "C"
import (
	"encoding/json"

	kitesession "github.com/nsvirk/gokitesession"
)

var client *kitesession.Client

func init() {
	client = kitesession.New()
}

//export GenerateTOTPValue
func GenerateTOTPValue(totpSecret *C.char) *C.char {
	totpSecretGo := C.GoString(totpSecret)

	totpValue, err := kitesession.GenerateTOTPValue(totpSecretGo)
	if err != nil {
		return C.CString("error:Failed to generate TOTP value: " + err.Error())
	}

	return C.CString(totpValue)
}

//export GenerateSession
func GenerateSession(userID, password, totpValue *C.char) *C.char {
	userIDGo := C.GoString(userID)
	passwordGo := C.GoString(password)
	totpValueGo := C.GoString(totpValue)

	session, err := client.GenerateSession(userIDGo, passwordGo, totpValueGo)
	if err != nil {
		return C.CString("error:" + err.Error())
	}

	jsonBytes, err := json.Marshal(session)
	if err != nil {
		return C.CString("error:Failed to marshal session: " + err.Error())
	}

	return C.CString(string(jsonBytes))
}

//export CheckEnctokenValid
func CheckEnctokenValid(enctoken *C.char) *C.char {
	enctokenGo := C.GoString(enctoken)

	isValid, err := client.CheckEnctokenValid(enctokenGo)
	if err != nil {
		return C.CString("error:" + err.Error())
	}

	if isValid {
		return C.CString("true")
	}
	return C.CString("false")
}

//export SetDebug
func SetDebug(debug C.int) {
	client.SetDebug(int(debug) != 0)
}

func main() {}
