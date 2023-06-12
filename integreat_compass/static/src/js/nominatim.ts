import { LngLat } from "maplibre-gl";

const apiBaseUrl = "http://nominatim.maps.tuerantuer.org/nominatim/";

export const getCoordinatesFromAddress = async (address: string): Promise<LngLat> => {
    const url = `${apiBaseUrl}search?format=json&q=${encodeURIComponent(address)}`;

    try {
        const response = await fetch(url);
        if (response.ok) {
            const data = await response.json();
            if (data.length > 0) {
                return new LngLat(parseFloat(data[0].lon), parseFloat(data[0].lat));
            }
            throw new Error("Address not found.");
        } else {
            throw new Error("Request failed.");
        }
    } catch (error) {
        throw new Error("Failed to fetch address coordinates.");
    }
};

export const getAddressFromCoordinates = async (ll: LngLat): Promise<string> => {
    const url = `${apiBaseUrl}reverse?format=json&lat=${ll.lat}&lon=${ll.lng}`;

    try {
        const response = await fetch(url);
        if (response.ok) {
            const data = await response.json();
            /* eslint-disable camelcase */
            let { house_number, postcode } = data.address;
            const { road, city, town, village, municipality } = data.address;

            if (!road || (!city && !town && !village && !municipality)) {
                return data.display_name;
            }

            house_number = house_number ? ` ${house_number}` : "";
            postcode = postcode ? `${postcode} ` : "";
            return `${road}${house_number}, ${postcode}${city || town || village}`;
        }
        throw new Error("Request failed.");
    } catch (error) {
        throw new Error("Failed to fetch address.");
    }
};
