using ConectaFapes.Application.DTOs.CadastroModalidadesBolsas.Request;
using ConectaFapes.Application.DTOs.CadastroModalidadesBolsas.Response;
using ConectaFapes.Test.Shared;
using System.Net;
using System.Text;
using System.Text.Json;
using Xunit;
using Xunit.Gherkin.Quick;

namespace ConectaFapes.Test.Steps
{
    [FeatureFile("../../../Features/modalidadebolsaFeature.feature")]
    [Collection(WebApplicationFactoryParameters.CollectionName)]
    public class ModalidadeBolsaStep : Xunit.Gherkin.Quick.Feature
    {
        private const string BASE_URL = "https://localhost:3000/api/modalidadebolsa/";
        private readonly WebApplicationFactory _factory;
        private readonly HttpClient _client;
        private HttpResponseMessage? _response;
        private ApiDataProvider _provider;

        public ModalidadeBolsaStep(WebApplicationFactory factory)
        {
            _factory = factory;
            _client = _factory.CreateClient(); 
            _provider = new ApiDataProvider(_client);
        }

        [Given("o usuário está autenticado no sistema")]
        public void GivenUsuarioAutenticado()
        {
            // Implement authentication logic here if needed.  For example:
            // _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", "your_token");
        }

        [When("ele acessa o endpoint de modalidades de bolsa")]
        public async Task WhenAcessaEndpointModalidadesBolsa()
        {
            _response = await _client.GetAsync(BASE_URL);
        }

        [Then("o sistema retorna todas as modalidades de bolsa cadastradas")]
        public async Task ThenRetornaTodasModalidades()
        {
            _response.EnsureSuccessStatusCode();
            var content = await _response.Content.ReadAsStringAsync();
            var modalidades = JsonSerializer.Deserialize<List<ModalidadeBolsaResponseDTO>>(content);

            Assert.NotNull(modalidades);
            Assert.NotEmpty(modalidades);
            Assert.True(modalidades.All(m => !string.IsNullOrEmpty(m.Nome)));
        }

        [When("ele cria uma nova modalidade de bolsa com sigla \"(.+)\" e nome \"(.+)\"")]
        public async Task WhenCriaNovaModalidade(string sigla, string nome)
        {
            var novaModalidade = new ModalidadeBolsaRequestDTO
            {
                Sigla = StringValidator.CheckEmptyString(sigla),
                Nome = StringValidator.CheckEmptyString(nome)
            };

            var content = new StringContent(JsonSerializer.Serialize(novaModalidade), Encoding.UTF8, "application/json");
            _response = await _client.PostAsync(BASE_URL, content);
        }

        [Then("o sistema retorna o ID da nova modalidade")]
        public async Task ThenRetornaIdNovaModalidade()
        {
            _response.EnsureSuccessStatusCode();
            var content = await _response.Content.ReadAsStringAsync();
            var novaModalidade = JsonSerializer.Deserialize<ModalidadeBolsaResponseDTO>(content);
            Assert.NotNull(novaModalidade?.Id);
        }

        [When("ele atualiza a modalidade de bolsa com ID \"(.+)\" com sigla \"(.+)\" e nome \"(.+)\"")]
        public async Task WhenAtualizaModalidade(string id, string sigla, string nome)
        {
            var modalidade = await _provider.GetEntityById<ModalidadeBolsaResponseDTO>("ModalidadeBolsa", id);
            if (modalidade == null)
            {
                throw new Exception($"Modalidade with ID '{id}' not found.");
            }

            modalidade.Sigla = StringValidator.CheckEmptyString(sigla);
            modalidade.Nome = StringValidator.CheckEmptyString(nome);

            var content = new StringContent(JsonSerializer.Serialize(modalidade), Encoding.UTF8, "application/json");
            _response = await _client.PutAsync($"{BASE_URL}{id}", content);
        }

        [Then("o sistema confirma a atualização da modalidade")]
        public async Task ThenConfirmaAtualizacaoModalidade()
        {
            _response.EnsureSuccessStatusCode();
            // Add assertions here to verify the updated data in the response.
        }

        [When("ele deleta a modalidade de bolsa com ID \"(.+)\"")]
        public async Task WhenDeletaModalidade(string id)
        {
            _response = await _client.DeleteAsync($"{BASE_URL}{id}");
        }

        [Then("o sistema confirma a deleção da modalidade")]
        public void ThenConfirmaDelecaoModalidade()
        {
            _response.EnsureSuccessStatusCode(); // Or check for HttpStatusCode.NoContent depending on API design.
        }

        [Given("I have access to the ModalidadeBolsa API")]
        public async Task IHaveAccessAPI()
        {
            var response = await _client.GetAsync(BASE_URL);
            response.EnsureSuccessStatusCode(); //More robust than Assert.Equal for API health check.
        }


        [When(@"I send a GET request to /modalidadebolsa/""(.+)""")]
        public async Task WhenISendAGetRequest(string modalidadeBolsaId)
        {
            _response = await _client.GetAsync(BASE_URL + modalidadeBolsaId);
        }

        [When(@"I send a POST request to /modalidadebolsa with the following ModalidadeBolsa details: ""(.+)"", ""(.+)""")]
        public async Task WhenISendAPostRequest(string sigla, string nome)
        {
            var modalidadeBolsa = new ModalidadeBolsaRequestDTO
            {
                Sigla = StringValidator.CheckEmptyString(sigla),
                Nome = StringValidator.CheckEmptyString(nome)
            };

            var content = new StringContent(JsonSerializer.Serialize(modalidadeBolsa), Encoding.UTF8, "application/json");
            _response = await _client.PostAsync(BASE_URL, content);
        }

        [When(@"I send a PUT request to /modalidadebolsa/""(.+)"" with the following ModalidadeBolsa details: ""(.+)"", ""(.+)""")]
        public async Task WhenISendAPutRequest(string modalidadeBolsaId, string sigla, string nome)
        {
            ModalidadeBolsaResponseDTO modalidadeBolsa = await _provider.GetEntityById<ModalidadeBolsaResponseDTO>("ModalidadeBolsa", modalidadeBolsaId);

            if (modalidadeBolsa == null)
            {
                throw new Exception($"Modalidade with ID '{modalidadeBolsaId}' not found.");
            }

            modalidadeBolsa.Sigla = StringValidator.CheckEmptyString(sigla);
            modalidadeBolsa.Nome = StringValidator.CheckEmptyString(nome);

            var content = new StringContent(JsonSerializer.Serialize(modalidadeBolsa), Encoding.UTF8, "application/json");
            _response = await _client.PutAsync(BASE_URL + modalidadeBolsaId, content);
        }

        [When(@"I send a DELETE request to /modalidadebolsa/""(.+)""")]
        public async Task WhenISendADeleteRequest(string modalidadeBolsaId)
        {
            _response = await _client.DeleteAsync(BASE_URL + modalidadeBolsaId);
        }

        [When(@"I send a PUT request to /modalidadebolsa/""(.+)""/ativar")]
        public async Task WhenISendAPutActiveRequest(string modalidadeBolsaId)
        {
            _response = await _client.PutAsync(BASE_URL + modalidadeBolsaId + "/ativar", null);
        }

        [When(@"I send a PUT request to /modalidadebolsa/""(.+)""/desativar")]
        public async Task WhenISendAPutDisableRequest(string modalidadeBolsaId)
        {
            _response = await _client.PutAsync(BASE_URL + modalidadeBolsaId + "/desativar", null);
        }

        [Then(@"the API response should be: ""(.+)""")]
        public void ThenApiResponse(string statusCodeString)
        {
            if (_response != null)
            {
                HttpStatusCode statusCode;
                if (Enum.TryParse<HttpStatusCode>(statusCodeString, out statusCode))
                {
                    Assert.Equal(statusCode, _response.StatusCode);
                }
                else
                {
                    Assert.True(false, $"Invalid HttpStatusCode: {statusCodeString}");
                }
            }
            else
            {
                Assert.True(false, "_response is null");
            }
        }
    }
}