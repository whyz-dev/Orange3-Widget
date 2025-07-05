let received = "";

serial.onDataReceived(serial.delimiters(Delimiters.NewLine), function () {
  basic.pause(50);
  received = serial.readUntil(serial.delimiters(Delimiters.NewLine));
  basic.pause(50);
  serial.writeLine(received);
});
