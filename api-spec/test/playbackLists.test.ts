import { Configuration, DefaultApi } from "../src/generated";
import swagger from "../build/swagger.json";
import Ajv from "ajv/dist/2020";
import addFormats from "ajv-formats";
const ajv = new Ajv({ strict: false });
addFormats(ajv);
ajv.addSchema(swagger, "swagger.json");

describe("playbackLists compliance test", () => {
  it.each(["18-805154", "18-645901", "18-786654"])(
    "fetch playbackList",
    async (playlistItemId: string) => {
      const playbackListItem = await api.getPlaylistItem({
        playlistItemId,
        context: "web",
        globalId: playlistItemId,
      });
      const valid = ajv.validate(
        { $ref: "swagger.json#/components/schemas/PlaylistItem" },
        JSON.parse(JSON.stringify(playbackListItem)),
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
    basePath: process.env.API_BASE_URL || "https://services.radio-canada.ca",
    headers: { "User-Agent": process.env.USER_AGENT || "" },
  }),
);
