import React, { useEffect, useState } from 'react';
import { fetchIcon } from '@/axios';
import styles from './icon.module.scss'
const IconComponent = ({ providerId }) => {
    const [iconHtml, setIconHtml] = useState('');
    useEffect(() => {
        const fetchIcon1 = async () => {
            const res = await fetchIcon(providerId)
            const html = await res;
            setIconHtml(html);
        };

        fetchIcon1()
    }, [providerId]);
    return <div dangerouslySetInnerHTML={{ __html: iconHtml }} className={styles.icon} />;
};

export default IconComponent;
