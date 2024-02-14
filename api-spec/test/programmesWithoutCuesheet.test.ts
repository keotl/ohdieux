import { Configuration, DefaultApi } from "../src/generated";
import swagger from "../build/swagger.json";
import Ajv from "ajv/dist/2020";
import addFormats from "ajv-formats";
const ajv = new Ajv({ strict: false });
addFormats(ajv);
ajv.addSchema(swagger, "swagger.json");

describe("programmesWithoutCuesheet compliance test", () => {
  it.each(["9887", "672", "3858", "3855", "8362"])(
    "get programme episode page",
    async (programmeId: string) => {
      const programmeEpisodes = await api.getProgrammeWithoutCuesheet({
        programmeId,
        pageNumber: 1,
        context: "web",
      });
      const valid = ajv.validate(
        { $ref: "swagger.json#/components/schemas/ProgrammeWithoutCuesheet" },
        JSON.parse(JSON.stringify(programmeEpisodes)),
      );
      if (ajv.errors) {
        console.log(ajv.errors);
      }
      expect(valid).toBeTruthy();
    },
  );
});

const api = new DefaultApi(
  new Configuration({
    basePath: "https://services.radio-canada.ca",
    headers: { "User-Agent": process.env.USER_AGENT || "" },
  }),
);
