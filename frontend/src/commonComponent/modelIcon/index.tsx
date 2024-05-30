import DimensionIcon from '@/assets/img/dimsionIcon.svg?react'
import FunctionCall from '@/assets/img/functionCallIcon.svg?react'
import InputTokenIcon from '@/assets/img/inputTokenIcon.svg?react'
import MaxBatchSizeIcon from '@/assets/img/maxBatchSizeIcon.svg?react'
import OutputTokenIcon from '@/assets/img/outputTokensIcon.svg?react'
import StreamIcon from '@/assets/img/streamIcon.svg?react'
import VisionInputIcon from '@/assets/img/visionInputIcon.svg?react'
import styles from './modelIcon.module.scss'
function ModelIcon(props: any) {
    const { properties, isShowText = true } = props;
    const IconReverse = {
        'embedding_size': <DimensionIcon />,
        'function_call': <FunctionCall />,
        'input_token_limit': <InputTokenIcon />,
        'max_batch_size': <MaxBatchSizeIcon />,
        'output_token_limit': <OutputTokenIcon />,
        'streaming': <StreamIcon />,
        'vision': <VisionInputIcon />
    }
    const textReverse = {
        'embedding_size': 'embedding size',
        'function_call': 'function call',
        'input_token_limit': 'input token limit',
        'max_batch_size': 'max batch size',
        'output_token_limit': 'output tokens limit',
        'streaming': 'stream',
        'vision': 'vision input'
    }
    return (
        <div className={styles['model-icon']}>
            {properties && Object.entries(properties).map(([key, value]) => {
                if (value !== false) {
                    return (
                       value ? <div key={key} className={`${styles.modelIcon} ${!isShowText && styles.modelIconText}`}>
                            {IconReverse[key as keyof typeof IconReverse]}
                            {isShowText && <>
                                <span className={styles.name}>{textReverse[key as keyof typeof textReverse]}</span>
                                {(typeof (value) !== 'boolean' && value) && <span className={styles.value}>:&nbsp;&nbsp;{value as string}</span>}</>}
                        </div> : null
                    );
                } else {
                    return null;
                }
            })}
        </div>
    );
}
export default ModelIcon;