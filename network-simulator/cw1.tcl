puts "======= Topology ======== "
puts ""
puts "      CBR0-UDP n0"
puts "                \\"
puts "                 n2 ---- n3"
puts "                /"
puts "      CBR1-TCP n1 "
puts ""
puts ""
if {$argc == 2 } {
    set type_agent  [lindex $argv 0]
    set fix_queue  [lindex $argv 1]
    if {$type_agent == "rfc" ||  $type_agent == "reno" } {
    	puts "Agent: $type_agent"
    } else {
        puts "Please use a correct agent type: rfc or reno"
        exit 1
    }
    if {$fix_queue == "true" ||  $fix_queue == "false" } {
    	puts "Fix Queue?: $fix_queue"
    } else {
        puts "Please say if you want to fix the queue (default size or size to 20): true or false"
        exit 1
    }
} else {
     puts "  Usage: ns agent (rfc|reno) fixqueue (true|false)"
    exit 1
}


# Creating the simulator object
set ns [new Simulator]
# Set simulation time
set simulation_time 200.0 


# File Related
set trailer .res
# File to store the trace
set tracefile_name trace_file$trailer
set trace_file [open $tracefile_name w]
$ns trace-all $trace_file
# File for saving the congestion window
set congestion_window_file_name congestion_window$trailer
set congestion_window_file [open $congestion_window_file_name w]
# File for saving the timeout values
if {$type_agent == "rfc"} {
    set timeout_file_name timeout$trailer
    set timeout_file [open $timeout_file_name w]
}



# Write trace and create new files from the original trace
proc finish {} {
        global ns trace_file congestion_window_file timeout_file
        $ns flush-trace
        close $trace_file
        close $congestion_window_file
        exit 0
}

# Record the congestion window for the tcp agent that sends every 0.1 secs.
proc record_tcp_agent_sender { } {
	global ns tcp1 congestion_window_file timeout_file type_agent

    set now [$ns now]

    set cwnd  [expr [$tcp1 set cwnd_]]
    set window  [expr [$tcp1 set window_]]

    puts $congestion_window_file "$now $cwnd $window"

    if {$type_agent == "rfc"} {
        set rtt  [expr [$tcp1 set rtt_]  * [$tcp1 set tcpTick_]]
        set srtt  [expr ([$tcp1 set srtt_] >> [$tcp1 set T_SRTT_BITS]) * [$tcp1 set tcpTick_]]
        set rttvar  [expr ([$tcp1 set rttvar_] >> [$tcp1 set T_RTTVAR_BITS]) * [$tcp1 set tcpTick_]]
        set rto [expr [$tcp1 set rto_]]
        puts $timeout_file "$now $rto $rtt $srtt $rttvar"
    }

	$ns at [expr $now+0.1] "record_tcp_agent_sender"
}

# Node 0 declaration
set n0 [$ns node]
set cbr0 [new Application/Traffic/Exponential]
set udp0 [new Agent/UDP]

# Node 1 declaration
set n1 [$ns node]
set cbr1 [new Application/Traffic/CBR]
if {$type_agent == "rfc"} {
    set tcp1 [new Agent/TCP/RFC793edu]
}
if {$type_agent == "reno"} {
    set tcp1 [new Agent/TCP/Reno]
}

# Node 2 declaration
set n2 [$ns node]

# Node 3 declaration
set n3 [$ns node]
set null_udp_connection [new Agent/Null]
set null_tcp_connection [new Agent/TCPSink]

# Duplex lines between nodes
$ns duplex-link $n0 $n2 250Kb 20ms DropTail
$ns duplex-link $n1 $n2 250Kb 20ms DropTail
$ns duplex-link $n2 $n3 50Kb 500ms DropTail

if {$fix_queue == "true"} {
    set cua [[$ns link $n2 $n3] queue]
    $cua set limit_ 20
}

# Node 0 configuration:
$ns attach-agent $n0 $udp0
$udp0 set class_ 0
$cbr0 set rate_ 0.05Mbps
$cbr0 attach-agent $udp0
$ns at 20.0 "$cbr0 start"
set udp_stop [expr {$simulation_time - 20}] 
$ns at udp_stop "$cbr0 stop"

# Node 1: configuration:
# Add Jacobson/Karels estimator
# We don't change values because source code already implements it with:
# δ1 = 1/8, δ2 = 1/4, μ = 1, ϕ = 4.
$tcp1 set class_ 1
set mss 1000
$tcp1 set packetSize_ $mss
$tcp1 set window_ 10
$tcp1 set tcpTick_ 0.01

if {$type_agent == "rfc"} {
    $tcp1 set add793jacobsonrtt_ true
    $tcp1 set add793karnrtt_ true
    $tcp1 set add793slowstart_ true
}

# Yeah, we messed up again, we forced the windowInit_ value to 1 on our RFC plots of the report...
# Our program would work the same way if we didn't force this value, but we did it to match the plots from the report.
if {$type_agent == "rfc" && $fix_queue == "false" } {
    $tcp1 set windowInit_ 1
}


$ns attach-agent $n1 $tcp1
$cbr1 set rate_ 0.05Mbps
$cbr1 attach-agent $tcp1
$ns at 0.0 "$cbr1 start"


# Node 3 configuration:
$ns attach-agent $n3 $null_udp_connection
$ns attach-agent $n3 $null_tcp_connection

# Connect 
$ns connect $udp0 $null_udp_connection
$ns connect $tcp1 $null_tcp_connection 

# Stop simulation at  200 s.
$ns at $simulation_time "finish"

#Run simulation
$ns at 0.0 "record_tcp_agent_sender"
$ns run
