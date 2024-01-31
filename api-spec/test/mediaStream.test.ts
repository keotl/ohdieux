import { Configuration, DefaultApi } from "../src/generated";
import swagger from "../build/swagger.json";
import Ajv from "ajv/dist/2020";
import addFormats from "ajv-formats";
const ajv = new Ajv({ strict: false });
addFormats(ajv);
ajv.addSchema(swagger, "swagger.json");

describe("mediaStream", () => {
  it.each(["8884220", "8884253", "8884876", "8881166", "8880063", "8879005"])(
    "fetch media stream url",
    async (mediaId: string) => {
      const mediaStream = await api.getMediaStream({
        idMedia: mediaId,
        tech: "progressive",
        appCode: "medianet",
        connectionType: "hd",
        deviceType: "ipad",
        multibitrate: "true",
        output: "json",
      });
      const valid = ajv.validate(
        { $ref: "swagger.json#/components/schemas/MediaStreamDescriptor" },
        JSON.parse(JSON.stringify(mediaStream)),
      );
      if (ajv.errors) {
        console.log(ajv.errors);
      }
      expect(valid).toBeTruthy();
    },
  );
});
const api = new DefaultApi(
  new Configuration({ basePath: "https://services.radio-canada.ca" }),
);
