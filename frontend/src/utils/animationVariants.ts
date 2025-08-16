// Animation Variants System for Blog-Poster Platform
import { Variants } from 'framer-motion'

export const fadeInUpVariants: Variants = {
  hidden: { 
    opacity: 0, 
    y: 20 
  },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { 
      duration: 0.5,
      ease: [0.25, 0.1, 0.25, 1]
    }
  }
}

export const staggerContainerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.3,
      when: "beforeChildren"
    }
  }
}

export const scaleRotateVariants: Variants = {
  hidden: { 
    scale: 0,
    rotate: -180,
    opacity: 0 
  },
  visible: { 
    scale: 1,
    rotate: 0,
    opacity: 1,
    transition: {
      type: "spring",
      stiffness: 260,
      damping: 20,
      duration: 0.6
    }
  }
}

export const slideVariants: Variants = {
  enter: (direction: number) => ({
    x: direction > 0 ? '100%' : '-100%',
    opacity: 0
  }),
  center: {
    zIndex: 1,
    x: 0,
    opacity: 1,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 30
    }
  },
  exit: (direction: number) => ({
    zIndex: 0,
    x: direction < 0 ? '100%' : '-100%',
    opacity: 0,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 30
    }
  })
}

export const heroAnimationVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.2,
      delayChildren: 0.1
    }
  }
}

export const heroChildVariants: Variants = {
  hidden: { 
    opacity: 0, 
    y: 50,
    scale: 0.9
  },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      type: "spring",
      damping: 15,
      stiffness: 100,
      duration: 0.8
    }
  }
}

export const cardHoverVariants: Variants = {
  idle: {
    scale: 1,
    rotateY: 0,
    rotateX: 0,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 30
    }
  },
  hover: {
    scale: 1.03,
    rotateY: 5,
    rotateX: -5,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 30
    }
  }
}

export const magneticButtonVariants: Variants = {
  hover: {
    scale: 1.05,
    transition: {
      type: "spring",
      stiffness: 400,
      damping: 25
    }
  },
  tap: {
    scale: 0.95,
    transition: {
      type: "spring",
      stiffness: 400,
      damping: 25
    }
  }
}

export const pulseVariants: Variants = {
  pulse: {
    scale: [1, 1.1, 1],
    opacity: [1, 0.8, 1],
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: "easeInOut"
    }
  }
}

export const navActiveIndicatorVariants: Variants = {
  active: {
    scale: 1,
    opacity: 1,
    transition: {
      type: "spring",
      stiffness: 350,
      damping: 30
    }
  },
  inactive: {
    scale: 0.8,
    opacity: 0,
    transition: {
      type: "spring",
      stiffness: 350,
      damping: 30
    }
  }
}

export const formFieldVariants: Variants = {
  idle: { 
    scale: 1,
    borderColor: "rgba(209, 213, 219, 1)"
  },
  focused: { 
    scale: 1.02,
    borderColor: "rgba(139, 92, 246, 1)",
    boxShadow: "0 0 0 3px rgba(139, 92, 246, 0.1)",
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 30
    }
  }
}

export const loadingSpinnerVariants: Variants = {
  spin: {
    rotate: 360,
    transition: {
      duration: 1,
      repeat: Infinity,
      ease: "linear"
    }
  }
}

export const draggableCardVariants: Variants = {
  drag: {
    scale: 1.1,
    zIndex: 10,
    filter: "drop-shadow(0 20px 25px rgba(0,0,0,0.15))",
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 25
    }
  },
  idle: {
    scale: 1,
    zIndex: 1,
    filter: "drop-shadow(0 4px 6px rgba(0,0,0,0.1))",
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 25
    }
  }
}

export const layoutAnimationVariants: Variants = {
  layout: {
    transition: {
      type: "spring",
      stiffness: 350,
      damping: 25
    }
  }
}

// Utility function to create custom stagger variants
export const createStaggerVariants = (
  staggerDelay: number = 0.1,
  childrenDelay: number = 0.3
): Variants => ({
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: staggerDelay,
      delayChildren: childrenDelay,
      when: "beforeChildren"
    }
  }
})

// Utility function to create custom slide variants
export const createSlideVariants = (distance: number = 100): Variants => ({
  enter: (direction: number) => ({
    x: direction > 0 ? distance : -distance,
    opacity: 0
  }),
  center: {
    x: 0,
    opacity: 1,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 30
    }
  },
  exit: (direction: number) => ({
    x: direction < 0 ? distance : -distance,
    opacity: 0,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 30
    }
  })
})