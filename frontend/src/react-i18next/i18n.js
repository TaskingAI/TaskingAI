import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import Backend from 'i18next-http-backend';
i18n
	.use(LanguageDetector)
	.use(initReactI18next)
	.use(Backend)
	.init({
		fallbackLng: "en",
		fallbackNS: ['translation'],
		lng: navigator.language,
		debug: true,
		interpolation: {
			escapeValue: false, // not needed for react as it escapes by default
		}
	});

export default i18n;