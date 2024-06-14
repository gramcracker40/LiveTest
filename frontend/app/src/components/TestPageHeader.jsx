import React from 'react';
import { Popover, PopoverButton, PopoverGroup, PopoverPanel, Transition } from "@headlessui/react";
import { Bars3Icon, ChevronDownIcon } from "@heroicons/react/24/outline";
import { BackButton } from "./BackButton";

export const TestPageHeader = ({ handleDateFormatting, test, setEditMode, setIsDeleteTestConfirmOpen, handleDownload, id, navigate }) => {
  return (
    <header className="bg-white">
      <nav className="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
        <div className="flex items-center gap-x-12">
          <BackButton className="px-8 py-3 text-sm font-semibold rounded-md shadow-sm bg-cyan-200 text-gray-700 hover:bg-cyan-300" />
        </div>
        <PopoverGroup className="hidden lg:flex lg:gap-x-12">
          <Popover className="relative">
            <PopoverButton className="flex items-center gap-x-1 text-sm font-semibold leading-6 text-gray-900">
              Test Options
              <ChevronDownIcon className="h-5 w-5 flex-none text-gray-400" aria-hidden="true" />
            </PopoverButton>

            <Transition
              enter="transition ease-out duration-200"
              enterFrom="opacity-0 translate-y-1"
              enterTo="opacity-100 translate-y-0"
              leave="transition ease-in duration-150"
              leaveFrom="opacity-100 translate-y-0"
              leaveTo="opacity-0 translate-y-1"
            >
              <PopoverPanel className="absolute z-10 mt-3 w-48 max-w-md overflow-hidden rounded-3xl bg-white shadow-lg ring-1 ring-gray-900/5">
                <div className="p-4">
                  <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                    <button
                      onClick={() => setEditMode(true)}
                      className="w-full text-left"
                    >
                      Edit Test
                    </button>
                  </div>
                  <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                    <button
                      onClick={() => setIsDeleteTestConfirmOpen(true)}
                      className="w-full text-left"
                    >
                      Delete Test
                    </button>
                  </div>
                  <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                    <button
                      onClick={() => handleDownload("blank")}
                      className="w-full text-left"
                    >
                      Download Blank Answer Sheet
                    </button>
                  </div>
                  <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                    <button
                      onClick={() => handleDownload("key")}
                      className="w-full text-left"
                    >
                      Download Key Answer Sheet
                    </button>
                  </div>
                </div>
              </PopoverPanel>
            </Transition>
          </Popover>
        </PopoverGroup>
        <div className="lg:hidden">
          <Popover className="relative">
            <PopoverButton className="inline-flex items-center justify-center p-2 text-gray-700">
              <Bars3Icon className="h-6 w-6" aria-hidden="true" />
            </PopoverButton>
            <Transition
              enter="transition ease-out duration-200"
              enterFrom="opacity-0 translate-y-1"
              enterTo="opacity-100 translate-y-0"
              leave="transition ease-in duration-150"
              leaveFrom="opacity-100 translate-y-0"
              leaveTo="opacity-0 translate-y-1"
            >
              <PopoverPanel className="absolute right-0 z-10 mt-3 w-48 max-w-md overflow-hidden rounded-3xl bg-white shadow-lg ring-1 ring-gray-900/5">
                <div className="p-4">
                  <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                    <button
                      onClick={() => setEditMode(true)}
                      className="w-full text-left"
                    >
                      Edit Test
                    </button>
                  </div>
                  <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                    <button
                      onClick={() => setIsDeleteTestConfirmOpen(true)}
                      className="w-full text-left"
                    >
                      Delete Test
                    </button>
                  </div>
                  <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                    <button
                      onClick={() => handleDownload("blank")}
                      className="w-full text-left"
                    >
                      Download Blank Answer Sheet
                    </button>
                  </div>
                  <div className="group relative flex gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50">
                    <button
                      onClick={() => handleDownload("key")}
                      className="w-full text-left"
                    >
                      Download Key Answer Sheet
                    </button>
                  </div>
                </div>
              </PopoverPanel>
            </Transition>
          </Popover>
        </div>
      </nav>
    </header>
  );
};
