erpbrasil-edoc-gen-download-schema -n paulistana -v v02 -u http://notadomilhao.prefeitura.sp.gov.br/arquivos/schemas.zip/@@download/file/schemas.zip
erpbrasil-edoc-gen-generate-python -m nfse -n paulistana -v v02 -i "PedidoEnvioLoteRPS_v01|PedidoConsultaLote_v01|RetornoEnvioLoteRPS_v01|RetornoConsulta_v01|RetornoInformacoesLote_v01" -d .
# O servico_enviar_lote_rps_envio_v03 foi necessário pois a classe EnviarLoteRpsEnvio
# não estava no arquivo de retorno.
