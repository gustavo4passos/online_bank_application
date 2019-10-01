Cliente:
Saque:
	s/conta/valor/\n\r

	Depósito:
	d/conta/valor/\n\r

	Transferência
	t/contaorigem/contadestino/valor/\n\r

	Saldo
	c/conta/\n\r

	Login
	l/conta/senha/\n\r

	Criar conta
	cc/rg/nome/n_conta_gerente/\n\r

Servidor\Respostas

	OK/\n\r

	BALANCE/nome/valor/\n\r

	LOGIN_SUCCESS/nome/saldo/\n\r

	INVALID_ACCOUNT/\n\r (Conta inexistente)

	INVALID_DESTINATION_ACCOUNT/\n\r

	INVALID_AMOUNT/\n\r

	BAD_REQUEST/\n\r (Mensagem mal formada)

	INVALID_ID/\n\r

	INVALID_NAME/\n\r

	NOT_A_MANAGER/\n\r
