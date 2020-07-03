package main

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"math"
	"net"
	"sync"
	"time"
)

type Host struct {
	con_type string
	hostname string
	port     int
	timeout  time.Duration
}

type HostExport struct {
	ConType  string
	Hostname string
	Port     int
	Open     bool
}

func main() {
	var hostname string
	flag.StringVar(&hostname, "hostname", "localhost", "Provide hostname (192.168.0.1, localhost, ...)")
	as_json := flag.Bool("json", false, "Exports open ports as json")
	flag.Parse()

	var online []HostExport

	// We scan all 2^16 ports, executing this as a goroutine might not work
	// because of the max filedescriptors available on your system
	var wg sync.WaitGroup
	TIMEOUT := time.Duration(5 * time.Second)
	for i := 0; i < int(math.Pow(2, 16)); i++ {
		wg.Add(1)
		func() {
			host, err := test_con(Host{"tcp", hostname, 1 + i, TIMEOUT})
			if err != nil {
				// Do nothing for now as we do not care about closed ports
			} else {
				if *as_json {
					online = append(online, HostExport{host.con_type, host.hostname, host.port, true})
				} else {
					fmt.Println("Found open port:", host.port, "on", host.hostname)
				}
			}
			wg.Done()
		}()
	}

	if *as_json {
		var json_data []byte
		json_data, err := json.MarshalIndent(online, "", "    ")
		if err != nil {
			fmt.Println(err)
		} else {
			fmt.Println(string(json_data))
		}
	}
}

func test_con(host Host) (Host, error) {
	con, err := net.DialTimeout(host.con_type, fmt.Sprint(host.hostname, ":", host.port), host.timeout)
	if err != nil {
		return host, errors.New(fmt.Sprint("Cannot open port ", host.port, " on ", host.hostname))
	} else {
		defer con.Close()
		return host, nil
	}
}
