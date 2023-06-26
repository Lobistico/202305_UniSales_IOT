export async function hookEstados() {
  const estados = await fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/`);
  if (estados.status === 200) {
    return estados.json();
  } else {
    return false;
  }
}

export async function hookMunicipios(estado: string) {

  const municipios = await fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${estado}/municipios/`);

  if (municipios.status === 200) {
    return municipios.json();
  } else {
    return false;
  }
}
