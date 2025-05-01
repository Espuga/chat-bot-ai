import { createI18n } from "vue-i18n";
import messages from "@intlify/unplugin-vue-i18n/messages";


export const i18n = createI18n({
    legacy: false,
    globalInjection: true,
    locale: 'en',
    fallbackLocale: 'en',
    availableLocales: ['en'],
    messages: messages,
    missing: (locale, key) => {
        if(key.length!=0) {
            console.warn(`[i18n] Missing translation for key "${key}" in locale "${locale}"`);
        }
        return key;
    },
});
