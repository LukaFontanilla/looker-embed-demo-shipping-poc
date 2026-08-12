import type { LookerLogoProps } from '../../../types'
import styles from './LookerLogo.module.css'

export function LookerLogo({ className = '', width = 24, height = 24, alt = 'Brand Logo', style, ...props }: LookerLogoProps) {
  return (
    <img
      src="/custom-logo.png"
      alt={alt}
      width={width}
      height={height}
      className={`${styles.lookerLogoIcon} looker-logo-icon ${className}`.trim()}
      style={{ objectFit: 'contain', ...style }}
      {...props}
    />
  )
}
