import {
    Input, Radio,RadioChangeEvent
} from 'antd';
import {  ChangeEvent } from 'react';
import styles from './actionDrawer.module.scss'
function ActionDrawer(props: any) {
    const { drawerTitle, schema,showTipError,onhandleTipError, onSchemaChange,onChangeAuthentication,Authentication,onRadioChange,radioValue,onChangeCustom,custom } = props
    const { TextArea } = Input
    const schemaPlaceholder = `{
        "openapi": "3.0.0",
        "info": {
          "title": "DALL-E 3 API",
          "version": "1.0.0",
          "description": "API for interacting with the DALL-E 3 image generation service"
        },
        "servers": [
          {
            "url": "https://api.openai.com/v1"
          }
        ],
        "paths": {
          "/images/generations": {
            "post": {
              "summary": "Generate images based on a text prompt",
              "operationId": "generateImages",
              "requestBody": {
                "required": true,
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/GenerateRequest"
                    }
                  }
                }
              },
              "responses": {
                "200": {
                  "description": "Image generation successful",
                  "content": {
                    "application/json": {
                      "schema": {
                        "$ref": "#/components/schemas/GenerateResponse"
                      }
                    }
                  }
                },
                "400": {
                  "description": "Bad request"
                },
                "401": {
                  "description": "Unauthorized"
                },
                "500": {
                  "description": "Server error"
                }
              },
              "security": [
                {
                  "apiKey": []
                }
              ]
            }
          }
        },
        "components": {
          "schemas": {
            "GenerateRequest": {
              "type": "object",
              "properties": {
                "model": {
                  "type": "string",
                  "enum": ["dall-e-3"],
                  "description": "Model used for generation"
                },
                "prompt": {
                  "type": "string",
                  "description": "Text prompt for image generation"
                },
                "n": {
                  "type": "integer",
                  "default": 1,
                  "description": "Number of images to generate"
                },
                "size": {
                  "type": "string",
                  "enum": ["1024x1024", "1792x1024", "1024x1792"],
                  "description": "Size of the generated image"
                }
              },
              "required": [
                "model",
                "prompt"
              ]
            },
            "GenerateResponse": {
              "type": "object",
              "properties": {
                "images": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "description": "Unique identifier for the generated image"
                      },
                      "url": {
                        "type": "string",
                        "format": "uri",
                        "description": "URL to access the generated image"
                      }
                    }
                  }
                }
              },
              "required": [
                "images"
              ]
            }
          },
          "securitySchemes": {
            "apiKey": {
              "type": "apiKey",
              "in": "header",
              "name": "Authorization"
            }
          }
        }
      }
    `
    const handleSchemaChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
        onSchemaChange(e.target.value)
        if (!e.target.value) {
            onhandleTipError(true)
        } else {
            onhandleTipError(false)
        }
    }
    const handleRadioChange = (e: RadioChangeEvent) => {
        onRadioChange(e.target.value)
    }
    const handleCustom = (e: ChangeEvent<HTMLInputElement>) => {
        onChangeCustom(e.target.value)
    }
    const titleCase = (str: string) => {
        const newStr = str.slice(0, 1).toUpperCase() + str.slice(1).toLowerCase();
        return newStr;
    }
    const hangleChangeAuthorization = (e: ChangeEvent<HTMLInputElement>) => {
        onChangeAuthentication(e.target.value)
    }
    return (
        <div className={styles['action-drawer']}>
            <div className={styles['top']}>
                <div className={styles['label']} style={{ marginTop: 0 }}>
                    <span className={styles['span']}> * </span>
                    <span>Schema</span>
                </div>
                {drawerTitle === 'Bulk Create Action' ?
                    <div className={styles['label-description']}>
                        The action JSON schema is compliant with
                        <a href="https://www.openapis.org/what-is-openapi" target="_blank" rel="noopener noreferrer" className={'href'}> the OpenAPI Specification</a>.
                        If there are multiple paths and methods in the schema, the service will create multiple
                        actions whose schema only has exactly one path and one method. We’ll use "operationId" and
                        "description" fields of each endpoint method as the name and description of the tool. Check
                        <a href="https://docs.tasking.ai/docs/guide/tool/action" target="_blank" rel="noopener noreferrer" className={'href'}> the documentation </a>
                        to learn more.
                    </div> :
                    <div className={styles['label-description']}> The action schema, Which is compliant with the OpenAPI
                        Specification. It should only have exactly one path and one method.</div>}

                <TextArea value={schema} placeholder={schemaPlaceholder}
                    onChange={(e) => handleSchemaChange(e)} showCount maxLength={32768}></TextArea>
                <div className={`${styles['desc-action-error']} ${showTipError ? styles.show : ''}`}>Schema is required</div>

            </div>
            <div className={styles['bottom']}>
                <div className={styles['label']}>
                    <span className={styles['span']}> * </span>
                    <span>Authentication</span>

                </div>
                <div className={styles['label-description']}>Authentication Type</div>
                <Radio.Group onChange={handleRadioChange} value={radioValue}>
                    <Radio value='none'>None</Radio>
                    <Radio value='basic'>Basic</Radio>
                    <Radio value='bearer'>Bearer</Radio>
                    <Radio value='custom'>Custom</Radio>
                </Radio.Group>
                {radioValue !== 'none' && <div style={{ display: 'flex', justifyContent: 'space-around', alignItems: 'center', margin: '15px 0' }}>
                    {radioValue !== 'custom' ? <span className={styles['desc-description']}>Authorization </span> : <Input placeholder='X-Custom' onChange={handleCustom} value={custom} style={{ width: '14%' }} />} <span className={styles['desc-description']}>:</span>  <Input prefix={<span style={{ color: '#999' }} >{radioValue !== 'custom' && titleCase(radioValue)}</span>} value={Authentication} placeholder='<Secret>' onChange={hangleChangeAuthorization} style={{ width: '83%' }}></Input>
                </div>
                }
            </div>
        </div>
    )
}
export default ActionDrawer