'use client'

import Link from 'next/link'
import { motion, Variants } from 'framer-motion'
import Icon from '@/components/ui/icon'
import { IconType } from '@/components/ui/icon/types'
import React, { useState } from 'react'

const EXTERNAL_LINKS = {
  documentation: 'https://agno.link/agent-ui',
  playground: 'https://app.agno.com/playground/agents',
  agno: 'https://agno.com'
}

const TECH_ICONS = [
  {
    type: 'nextjs' as IconType,
    position: 'left-0',
    link: 'https://nextjs.org',
    name: 'Next.js',
    zIndex: 10
  },
  {
    type: 'shadcn' as IconType,
    position: 'left-[15px]',
    link: 'https://ui.shadcn.com',
    name: 'shadcn/ui',
    zIndex: 20
  },
  {
    type: 'tailwind' as IconType,
    position: 'left-[30px]',
    link: 'https://tailwindcss.com',
    name: 'Tailwind CSS',
    zIndex: 30
  }
]

interface ActionButtonProps {
  href: string
  variant?: 'primary'
  text: string
}

const ActionButton = ({ href, variant, text }: ActionButtonProps) => {
  const baseStyles =
    'px-4 py-2 text-sm transition-colors font-dmmono tracking-tight'
  const variantStyles = {
    primary: 'border border-border hover:bg-neutral-800 rounded-xl'
  }

  return (
    <Link
      href={href}
      target="_blank"
      className={`${baseStyles} ${variant ? variantStyles[variant] : ''}`}
    >
      {text}
    </Link>
  )
}

const ChatBlankState = () => {
  const [hoveredIcon, setHoveredIcon] = useState<string | null>(null)

  // Animation variants for the icon
  const iconVariants: Variants = {
    initial: { y: 0 },
    hover: {
      y: -8,
      transition: {
        type: 'spring',
        stiffness: 150,
        damping: 10,
        mass: 0.5
      }
    },
    exit: {
      y: 0,
      transition: {
        type: 'spring',
        stiffness: 200,
        damping: 15,
        mass: 0.6
      }
    }
  }

  // Animation variants for the tooltip
  const tooltipVariants: Variants = {
    hidden: {
      opacity: 0,
      transition: {
        duration: 0.15,
        ease: 'easeInOut'
      }
    },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.15,
        ease: 'easeInOut'
      }
    }
  }

  return (
    <section
      className="font-geist flex flex-col items-center text-center"
      aria-label="Welcome message"
    >
      <div className="flex max-w-3xl flex-col gap-y-8">
        <motion.h1
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="text-3xl font-[600] tracking-tight"
        >
          <div className="flex items-center justify-center gap-x-2 whitespace-nowrap font-medium">
            <span className="flex items-center font-[600]">
              Bienvenido a EtherIA el agente de AI desarrollado por
            </span>
            <span className="inline-flex translate-y-[10px] scale-125 items-center transition-transform duration-200 hover:rotate-6">
              <img
                src="https://periferiaitgroup.com/wp-content/uploads/2024/12/periferia-it-group.png"
                alt="My Custom Image"
                className="h-6 w-6"
              />
            </span>
          </div>
        </motion.h1>
      </div>
    </section>
  )
}

export default ChatBlankState
