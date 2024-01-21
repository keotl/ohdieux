import { Configuration, DefaultApi } from "../src/generated";
import swagger from "../build/swagger.json";
import Ajv from "ajv/dist/2020";
import addFormats from "ajv-formats";
const ajv = new Ajv({ strict: false });
addFormats(ajv);
ajv.addSchema(swagger, "swagger.json");

describe("programmesWithoutCuesheet", () => {
  it("get programme episode page", async () => {
    const programmeEpisodes = await api.getProgrammeWithoutCuesheet({
      programmeId: "9887",
      pageNumber: 1,
    });
    const valid = ajv.validate(
      { $ref: "swagger.json#/components/schemas/ProgrammeWithoutCuesheet" },
      JSON.parse(JSON.stringify(programmeEpisodes)),
    );
    if (ajv.errors) {
      console.log(ajv.errors);
    }
    expect(valid).toBeTruthy();
  });
});

const api = new DefaultApi(
  new Configuration({ basePath: "https://services.radio-canada.ca" }),
);
