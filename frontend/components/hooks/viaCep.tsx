export default async function hookCep ( pCep: string) {
  try {
    const resultCep = await fetch(`https://viacep.com.br/ws/${pCep}/json/`);
    if(resultCep.status === 200) {
      return await resultCep.json();
    }
    else if (resultCep.status === 400){
      return false;
    }
  } catch (error) {

    return false;
  }
}