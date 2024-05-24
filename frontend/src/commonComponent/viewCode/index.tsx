import styles from './viewCode.module.scss'
import CloseIcon from '@/assets/img/x-close.svg?react'
import { Modal, Input } from 'antd'
import { useEffect, useState } from 'react'
import ArrowTop from '../../assets/img/ArrowBottom.svg?react'
import ArrowTopIcons from '@/assets/img/ArrowTopIcons.svg?react'
import ArrowBottomIcons from '@/assets/img/ArrowBottom.svg?react'
import MarkdownMessageBlock from '@taskingai/taskingai-markdown'
import { v4 as uuidv4 } from 'uuid'

import './index.css'
// import '../../components/playground/index.css'
const ViewCode = (props: any) => {
    const { open, handleClose, data } = props
    const [flattenedData, setFlattenedData] = useState<any>([])
    const [uniqueLanguages, setUniqueLanguages] = useState<any>([]);
    useEffect(() => {
        if (data) {
            const flattenedData: any = [];
            data.forEach((language: any) => {
                language.parts.forEach((part: any) => {
                    part.templates.forEach((template: any) => {
                        flattenedData.push({
                            language_name: language.language_name,
                            part_name: part.part_name,
                            template_name: template.template_name,
                            content: template.content,
                            originalContent: template.content,
                            variables: template.variables,
                            id: uuidv4()
                        });
                    });
                });
            });
            setFlattenedData(flattenedData);
        }
    }, [data])
    useEffect(() => {
        if (flattenedData.length > 0) {
            const name = Array.from(new Set(flattenedData.map((item: any) => item.language_name)))[0]
            // const partName = flattenedData[0].part_name
            setLanguageName(name)
            const newSetList = Array.from(new Set(flattenedData.filter((item: any) => item.language_name === name).map((item: any) => item.part_name))) || []
            setFilteredParts(Array.from(new Set(flattenedData.filter((item: any) => item.language_name === name))) || []);
            const templateName:any = Array.from(new Set(flattenedData.filter((item: any) => item.language_name === name)))[0]
            if(templateName) {
                setTemplateName(templateName.template_name)
                setRightContent([flattenedData.filter((item: any) => item.template_name === templateName.template_name)[0]]);
            }
            setUniqueParts(newSetList)
            const list: any = []
            newSetList.forEach(() => {
                list.push(false)
            })
            list[0] = true
            setIsShowSubMenu(list)
            setUniqueLanguages(Array.from(new Set(flattenedData.map((item: any) => item.language_name))))
        }
    }, [flattenedData])
    const [selectedLanguage, setSelectedLanguage] = useState(uniqueLanguages[0] || null);
    const [uniqueParts, setUniqueParts] = useState<any>([]);
    const [filteredParts, setFilteredParts] = useState<any>([]);
    const [rightContent, setRightContent] = useState<any>([]);
    const [templateName, setTemplateName] = useState<any>('')
    const [isShowSubMenu, setIsShowSubMenu] = useState<any>([])
    const [languageName, setLanguageName] = useState<any>([]);
    const [replacements, setReplacements] = useState({});
    const handleLanguageSelect = (language: any) => {
        setLanguageName(language)
        const newSetList = Array.from(new Set(flattenedData.filter((item: any) => item.language_name === language).map((item: any) => item.part_name))) || []
        setUniqueParts(newSetList)
        const list: any = []
        newSetList.forEach(() => {
            list.push(false)
        })
        list[0] = true
        setIsShowSubMenu(list)
        setSelectedLanguage(language);
        setFilteredParts(Array.from(new Set(flattenedData.filter((item: any) => item.language_name === language))) || []);
        const templateName:any = Array.from(new Set(flattenedData.filter((item: any) => item.language_name === language)))[0]
        if(templateName) {
            setTemplateName(templateName.template_name)
            setRightContent([flattenedData.filter((item: any) => item.template_name === templateName.template_name && item.language_name === language)[0]]);
        }
    };
    const handlePartSelect = (part: any) => {
        setReplacements({})
        setTemplateName(part.template_name)
        setRightContent(filteredParts.filter((item: any) => item.template_name === part.template_name));
    }
    useEffect(() => {
        if (uniqueLanguages.length > 0) {
            setSelectedLanguage(uniqueLanguages[0]);
        }
    }, [uniqueLanguages]);
    const RecursiveMenu = ({ items }: any) => {
        return (
            <ul style={{ paddingLeft: 0 }}>
                {items.map((item: any) => (
                    <li key={item.id} style={{ display: 'flex' }}>
                        <div >{item.title} {item.level === 2 && <ArrowTop />}</div>
                        {item.children && <RecursiveMenu items={item.children} />}
                    </li>
                ))}
            </ul>
        );
    };
    const handlePartClick = (index: number) => {
        setIsShowSubMenu((prev: any) => {
            const list = [...prev]
            list.forEach((_item: any, i: number) => {
                if (i !== index) {
                    list[i] = false
                } else {
                    list[index] = !list[index]
                }
            })
            return list
        })
    }
    const handleValue = (e: any, itemId: string, variable: any) => {
        const newValue = `${e.target.value}`;
        const newReplacements: any = {
            ...replacements,
            [variable]: newValue
        };
        setReplacements(newReplacements);
        setRightContent((prev: any) => prev.map((item: any) => {
            if (item.id === itemId) {
                let newContent = item.originalContent;
                Object.keys(newReplacements).forEach(key => {
                    const escapedKey = key.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
                    const regex = new RegExp(escapedKey, 'g');
                    newContent = newContent.replace(regex, newReplacements[key]); 
                });
                return { ...item, content: newContent };
            }
            return item;
        }));
    }

    return (
        <Modal centered width={1280} open={open} title='View Code' className={`${styles.modal} view-code-component`} onCancel={handleClose} footer={null} closeIcon={<CloseIcon />}>
            <div style={{ display: 'flex', width: '100%', flexShrink: 0,height:'732px' }}>
                <div className={styles.silder}>
                    {uniqueLanguages.map((language: any) => (
                        <div className={`${styles['first-menu']} ${language === languageName && styles['selected-menu']}`} key={language} onClick={() => handleLanguageSelect(language)}>
                            {language}
                        </div>
                    ))}
                </div>

                <div className={styles.content}>
                    {selectedLanguage && uniqueParts.map((part: any, index: number) => (
                        <div key={part} style={{ width: '180px' }}>
                            <div className={styles['second-menu']} onClick={() => handlePartClick(index)}>{part} {isShowSubMenu[index] ? <ArrowTopIcons /> : <ArrowBottomIcons />}  </div>
                            {isShowSubMenu[index] && <ul>
                                {filteredParts.filter((item: any) => item.part_name === part).map((template: any) => (
                                    <li  className={`${styles['third-menu']} ${templateName === template.template_name && styles['selected-menu']}`} key={template.template_name} onClick={() => handlePartSelect(template)}>{template.template_name}</li>
                                ))}
                            </ul>}
                        </div>
                    ))}
                </div>
                <div className={styles['content-right']}>
                    <>
                        {rightContent.map((item: any) => (
                            <div key={item.id}>
                                <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '24px' }}>
                                    {item.variables.map((variable: any,index: number) => (
                                        <div className={styles.variables} key={index}>
                                            <div className={styles['variables-left']}>{variable.replace(/\$\$(.*?)\$\$/g, (_match: any, p1: any) => p1.toLowerCase())}</div>
                                            <Input type="text" onChange={(e) => handleValue(e, item.id, variable)} className={styles['variable-input']} placeholder={`Enter ${variable.replace(/\$\$(.*?)\$\$/g, (_match: any, p1: any) => p1.toLowerCase())}`} />
                                        </div>
                                    ))}
                                </div>
                                <MarkdownMessageBlock message={item.content}></MarkdownMessageBlock>
                            </div>
                        ))}
                    </>
                </div>
            </div>
        </Modal>
    )
}
export default ViewCode