function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = JSON.parse(e.postData.contents);
  
  if (data.tipo == "cadastro") {
    sheet.appendRow([
      new Date(),                    // timestamp
      data.nome,                     // nome
      data.sexo,                     // sexo
      data.email,                    // email
      data.celular                   // celular
    ]);
  }
  
  else if (data.tipo == "resumo") {
    sheet.appendRow([
      new Date(),                    // timestamp (coluna A - tipo?)
      data.nome,                     // B - nome
      data.area,                     // C - area
      data.habilidades_marcadas,     // D - habilidades_marcadas
      data.contagem_habilidades_marcada,  // E - contagem
      data.total_habilidades,        // F - total_habilidades
      data.Resultado,                // G - Resultado (percentual)
      data.conclusao                 // H - conclusao (Apto/Não Apto)
    ]);
  }
  
  return ContentService.createTextOutput("OK");
}
