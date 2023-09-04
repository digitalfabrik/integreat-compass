import { FullscreenControl, LngLat, LngLatLike, Map, MapOptions, MapMouseEvent, Marker } from "maplibre-gl";
import { getAddressFromCoordinates, getCoordinatesFromAddress } from "./nominatim";
import "maplibre-gl/dist/maplibre-gl.css";

const getCoordinateInputFields = () => {
    const latitudeInput = document.getElementById("id_location-lat") as HTMLInputElement;
    const longitudeInput = document.getElementById("id_location-long") as HTMLInputElement;
    return [latitudeInput, longitudeInput];
};

const getCoordinates = (): [LngLatLike | null, boolean | null] => {
    const [latitudeInput, longitudeInput] = getCoordinateInputFields();
    if (latitudeInput?.value && longitudeInput?.value) {
        return [new LngLat(longitudeInput.valueAsNumber, latitudeInput.valueAsNumber), false];
    }

    const urlParams = new URLSearchParams(window.location.search);
    const [latParam, longParam] = [urlParams.get("lat"), urlParams.get("long")];
    if (latParam && longParam) {
        latitudeInput.value = latParam;
        longitudeInput.value = longParam;
        return [new LngLat(parseFloat(longParam), parseFloat(latParam)), true];
    }
    return [null, null];
};

export const updateField = (fieldName: string, value: string) => {
    const field = document.getElementById(`id_location-${fieldName}`) as HTMLInputElement;
    if (value !== null && field.value !== value) {
        field.value = value;
    }
};

const updateCoordinates = (marker: Marker) => {
    const lngLat = marker.getLngLat();
    const maxCoordinatePrecision = 7;
    updateField("long", lngLat.lng.toFixed(maxCoordinatePrecision));
    updateField("lat", lngLat.lat.toFixed(maxCoordinatePrecision));

    getCoordinateInputFields()[0].dispatchEvent(new Event("change"));
};

const initializeMap = (container: HTMLElement, searchBar: HTMLInputElement, zoomAdjust?: number) => {
    /* eslint-disable-next-line no-magic-numbers */
    const centerOfGermany = [10.3873, 51.215];
    const centeredZoom = 16;
    const minAddressLength = 3;
    const [coordinates, requiresUpdate] = getCoordinates();

    const options = {
        container,
        style: "https://maps.tuerantuer.org/styles/integreat/style.json",
    } as MapOptions;

    if (coordinates) {
        options.center = coordinates;
        options.zoom = centeredZoom + (zoomAdjust ?? 0);
    } else {
        options.center = centerOfGermany as LngLatLike;
        options.zoom = 5;
    }

    const map = new Map(options);
    const marker = new Marker();
    marker.setDraggable(true);
    map.on("load", map.resize);
    map.addControl(new FullscreenControl({ container }));

    const updateAddress = () => {
        getAddressFromCoordinates(marker.getLngLat()).then((address) => {
            /* eslint-disable-next-line no-param-reassign */
            searchBar.value = address;
        });
    };

    if (coordinates) {
        marker.setLngLat(coordinates).addTo(map);
        if (requiresUpdate) {
            updateAddress();
        }
    }

    const placeMarkerAtAddress = () => {
        if (searchBar.value.trim().length > minAddressLength) {
            getCoordinatesFromAddress(searchBar.value).then((ll) => {
                marker.setLngLat(ll).addTo(map);
                map.setCenter(ll);
                map.setZoom(centeredZoom);
                updateCoordinates(marker);
            });
        }
    };
    map.on("click", (event: MapMouseEvent) => {
        marker.setLngLat(event.lngLat).addTo(map);
        updateCoordinates(marker);
        updateAddress();
    });
    marker.on("dragend", () => {
        updateCoordinates(marker);
        updateAddress();
    });

    searchBar.addEventListener("focusout", placeMarkerAtAddress);
    searchBar.addEventListener("keypress", (event: KeyboardEvent) => {
        if (event.key === "Enter") {
            event.preventDefault();
            placeMarkerAtAddress();
        }
    });
};

const initializeOfferMap = () => {
    const container = document.getElementById("map");
    const searchBar = document.getElementById("id_location-address") as HTMLInputElement;
    const modeSwitch = document.querySelector(".mode_type") as HTMLElement;
    const onlineCheckbox = document.getElementById("id_offer-mode_type_0") as HTMLInputElement;

    if (!container || !searchBar || !modeSwitch || !onlineCheckbox) {
        return;
    }

    initializeMap(container, searchBar);

    let isAutomaticEventFire = true;
    modeSwitch.addEventListener("click", () => {
        const locationFormWrapper = document.getElementById("location-form-wrapper");
        if (!locationFormWrapper) {
            return;
        }

        if (onlineCheckbox.checked) {
            locationFormWrapper.classList.add("hidden");
        } else {
            locationFormWrapper.classList.remove("hidden");
            if (!isAutomaticEventFire) {
                searchBar.focus();
                window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
            }
            isAutomaticEventFire = false;
        }

        const [lat, long] = getCoordinateInputFields();
        lat.required = !onlineCheckbox.checked;
        long.required = !onlineCheckbox.checked;
        searchBar.required = !onlineCheckbox.checked;
    });
    modeSwitch.dispatchEvent(new Event("click"));
};

const initializeFilterMap = () => {
    const container = document.getElementById("filter-map");
    const searchBar = document.getElementById("filter-address") as HTMLInputElement;
    const reset = document.getElementById("location-filter-reset");

    if (!container || !searchBar || !reset) {
        return;
    }

    const params = new URLSearchParams(window.location.search);
    const radius = params.get("radius");
    const radiusToZoom = (radius: string | null) => {
        const zoomAdjustFactor = 1.5;
        return -Math.log(parseFloat(radius ?? "0") ** 2 * zoomAdjustFactor);
    };
    initializeMap(container, searchBar, radiusToZoom(radius));

    reset.addEventListener("click", () => {
        console.log("here");
        params.delete("radius");
        (document.querySelector('input[name="radius"]:checked') as HTMLInputElement).checked = false;
        updateField("lat", "");
        updateField("long", "");
        const [latitudeInput, _] = getCoordinateInputFields();
        latitudeInput.dispatchEvent(new Event("change"));
    });
};

window.addEventListener("load", () => {
    initializeOfferMap();
    initializeFilterMap();
});
