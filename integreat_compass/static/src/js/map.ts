import { FullscreenControl, LngLat, LngLatLike, Map, MapOptions, MapMouseEvent, Marker } from "maplibre-gl";
import { getAddressFromCoordinates, getCoordinatesFromAddress } from "./nominatim";
import "maplibre-gl/dist/maplibre-gl.css";

const getCoordinateInputFields = () => {
    const latitudeInput = document.getElementById("id_location-lat") as HTMLInputElement;
    const longitudeInput = document.getElementById("id_location-long") as HTMLInputElement;
    return [latitudeInput, longitudeInput];
};

const getCoordinates = () => {
    const [latitudeInput, longitudeInput] = getCoordinateInputFields();
    if (latitudeInput.value && longitudeInput.value) {
        return new LngLat(longitudeInput.valueAsNumber, latitudeInput.valueAsNumber);
    }
    return null;
};

export const updateField = (fieldName: string, value: number) => {
    const field = document.getElementById(`id_location-${fieldName}`) as HTMLInputElement;
    if (value && field.value !== value.toString()) {
        field.value = value.toString();
    }
};

const updateCoordinates = (marker: Marker) => {
    const lngLat = marker.getLngLat();
    updateField("long", lngLat.lng);
    updateField("lat", lngLat.lat);
};

window.addEventListener("load", () => {
    /* eslint-disable-next-line no-magic-numbers */
    const centerOfGermany = [10.3873, 51.215];
    const centeredZoom = 16;
    const minAddressLength = 3;

    const coordinates = getCoordinates();
    const container = document.getElementById("map");
    const searchBar = document.getElementById("id_location-address") as HTMLInputElement;
    const modeSwitch = document.querySelector(".mode_type") as HTMLElement;
    const onlineCheckbox = document.getElementById("id_offer-mode_type_0") as HTMLInputElement;

    if (!container || !searchBar || !onlineCheckbox) {
        return;
    }

    const options = {
        container,
        style: "https://maps.tuerantuer.org/styles/integreat/style.json",
    } as MapOptions;

    if (coordinates) {
        options.center = coordinates;
        options.zoom = centeredZoom;
    } else {
        options.center = centerOfGermany as LngLatLike;
        options.zoom = 5;
    }

    const map = new Map(options);
    const marker = new Marker();
    marker.setDraggable(true);
    map.on("load", map.resize);
    map.addControl(new FullscreenControl({ container }));

    if (coordinates) {
        marker.setLngLat(coordinates).addTo(map);
    }

    const updateAddress = () => {
        getAddressFromCoordinates(marker.getLngLat()).then((address) => {
            searchBar.value = address;
        });
    };

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
    searchBar.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            placeMarkerAtAddress();
        }
    });

    modeSwitch.addEventListener("click", () => {
        const locationFormWrapper = document.getElementById("location-form-wrapper");
        if (!locationFormWrapper) {
            return;
        }

        if (onlineCheckbox.checked) {
            locationFormWrapper.classList.add("hidden");
        } else {
            locationFormWrapper.classList.remove("hidden");
        }
    });
    modeSwitch.dispatchEvent(new Event("click"));
});
