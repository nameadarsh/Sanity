export const Skeleton = ({ className = '', width, height }) => {
  return (
    <div
      className={`shimmer rounded ${className}`}
      style={{
        width: width || '100%',
        height: height || '1rem',
      }}
    />
  )
}

export const CardSkeleton = () => {
  return (
    <div className="card animate-pulse">
      <Skeleton height="2rem" className="mb-4" />
      <Skeleton height="1rem" className="mb-2" />
      <Skeleton height="1rem" width="80%" />
    </div>
  )
}

export const TextSkeleton = ({ lines = 3 }) => {
  return (
    <div className="space-y-2">
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton
          key={i}
          height="1rem"
          width={i === lines - 1 ? '60%' : '100%'}
        />
      ))}
    </div>
  )
}

