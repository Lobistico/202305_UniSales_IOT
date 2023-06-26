export default function GetDay(data: Date) {

  const diaDaSemana = new Date(data).getDay();

  // Convertendo o número retornado para o dia da semana em formato de texto
  const diasDaSemana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
  return diasDaSemana[diaDaSemana];

}