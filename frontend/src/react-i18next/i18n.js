import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import { resources } from './resources';
i18n
	.use(LanguageDetector)
	.use(initReactI18next)
	.init({
		resources,
		fallbackLng: "en",
		lng: navigator.language,
		debug: true,
		interpolation: {
			escapeValue: false, // not needed for react as it escapes by default
		}
	});

export default i18n;