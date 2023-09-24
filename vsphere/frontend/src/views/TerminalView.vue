<template>
  <div id="terminal"></div>
</template>

<script>
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';

export default {
  name: 'TerminalView',

  mounted() {
    const term = new Terminal();
    term.open(this.$el);

    const socket = new WebSocket('ws://localhost:8000/ws'); 
    socket.onmessage = (event) => {
      term.write(event.data);
    };

    term.onData((data) => {
      socket.send(data);
    });

    socket.onclose = (event) => {
      term.write('\r\n*** SSH DISCONNECTED ***\r\n');
    };
  }
}
</script>
